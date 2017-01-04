import re
from datetime import datetime
import os

from django.core.management.base import BaseCommand
from requests_oauthlib import OAuth1Session
import requests

from flights.models import Trip, Segment, TrainSegment, TimeStamp

class Command(BaseCommand):
    GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
    DEFAULT_TIMEZONE_OFFSET = '-04:00'

    # fffffff
    DURATION_REGEXS = [
        r'(?:(\d+) hours)? (\d+) minutes',
        r'(?:(\d+)h, )?(\d+)m',
        r'(\d+):(\d+)',
    ]

    def _get_datetime(self, date_obj):
        return datetime.strptime(
            '{} {} {}'.format(
                date_obj['date'],
                date_obj['time'],
                date_obj.get('utc_offset',
                    self.DEFAULT_TIMEZONE_OFFSET).replace(':', '')),
            '%Y-%m-%d %H:%M:%S %z'
        )

    def _get_duration(self, flight):
        duration = flight.get('duration')
        if duration is not None:
            for regex in self.DURATION_REGEXS:
                match = re.match(regex, duration)
                if match is not None:
                    break
            if match is not None:
                hrs, mins = match.groups()
                if hrs is None:
                    return int(mins)
                return int(hrs) * 60 + int(mins)

        # calculate by hand
        start_time = self._get_datetime(flight['StartDateTime'])
        end_time = self._get_datetime(flight['EndDateTime'])

        return (end_time - start_time).seconds * 60

    def _get_distance(self, distance):
        if distance is None:
            return None
        match = re.match('([\d,]+) (\w+)', distance)
        if match is None:
            raise ValueError("Can't parse distance " + distance)
        distance, units = match.groups()
        distance = int(distance.replace(',',''))
        if units.lower() == 'miles':
            return distance
        elif units.lower() == 'km':
            return round(distance * 0.621)
        else:
            raise ValueError("Can't parse distance unit " + units)

    def _make_segment(self, trip, flight):
        segment = {
            'trip': trip,
            'start_airport': flight['start_airport_code'],
            'start_city': flight['start_city_name'],
            'start_time': self._get_datetime(flight['StartDateTime']),
            'start_ltlng': '{},{}'.format(flight['start_airport_latitude'],
                flight['start_airport_longitude']),

            'end_airport': flight['end_airport_code'],
            'end_city': flight['end_city_name'],
            'end_time': self._get_datetime(flight['EndDateTime']),
            'end_ltlng': '{},{}'.format(flight['end_airport_latitude'],
                flight['end_airport_longitude']),

            'airline': flight['marketing_airline'],
            'flight_number': flight['marketing_flight_number'],
            'distance_miles': self._get_distance(flight.get('distance')),
            'duration_mins': self._get_duration(flight),
        }
        self.stdout.write(
            '  Adding {} {} for trip {}'.format(
            segment['airline'],
            segment['flight_number'],
            trip.name,
            )
        )
        Segment.objects.update_or_create(id=flight['id'], defaults=segment)

    def _get_location(self, station_name, segment_obj):
        lat = None
        lng = None
        city = None
        if segment_obj is not None and 'city' in segment_obj and 'latitude' in segment_obj:
            city = segment_obj['city']
            lat = segment_obj['latitude']
            lng = segment_obj['longitude']
        else:
            city = None
            if segment_obj is not None and 'address' in segment_obj:
                city = segment_obj['address']
            else:
                city = station_name
            city, lat, lon = self._geocode_city(city)
        return city, '{},{}'.format(lat, lng)

    def _geocode_city(self, query):
        r = requests.get(self.GEOCODE_URL,
                         params={'key': os.environ['GOOGLE_API_KEY'],
                                 'address': query})
        r.raise_for_status()
        result = r.json()['results'][0]
        city = next(x for x in result['address_components'] if 'locality' in x['types'])
        if isinstance(city, dict) and 'long_name' in city:
            city = city['long_name']
        loc = result['geometry']['location']
        return city, loc['lat'], loc['lng']

    def _make_train_segment(self, trip, train):
        start_city, start_latlng = self._get_location(train['start_station_name'],
                                                      train.get('StartStationAddress'))
        end_city, end_latlng = self._get_location(train['end_station_name'],
                                                  train.get('EndStationAddress'))
        segment = {
            'trip': trip,
            'start_station': train['start_station_name'],
            'start_city': start_city,
            'start_time': self._get_datetime(train['StartDateTime']),
            'start_ltlng': start_latlng,

            'end_station': train['end_station_name'],
            'end_city': end_city,
            'end_time': self._get_datetime(train['EndDateTime']),
            'end_ltlng': end_latlng,

            'carrier': train['carrier_name'],
            'train_number': train['train_number'],
            'duration_mins': self._get_duration(train),
        }

        self.stdout.write(
            '  Adding {} {} for trip {}'.format(
            segment['carrier'],
            segment['train_number'],
            trip.name,
            )
        )
        obj = TrainSegment.objects.update_or_create(id=train['id'], defaults=segment)

    def handle(self, *args, **kwargs):
        tripit = OAuth1Session(
                os.environ['TRIPIT_OAUTH_KEY'],
                client_secret=os.environ['TRIPIT_OAUTH_SECRET'],
                resource_owner_key=os.environ['TRIPIT_CONSUMER_KEY'],
                resource_owner_secret=os.environ['TRIPIT_CONSUMER_SECRET'],
                )
        tripit.params.update({'format': 'json'})

        modified_since = TimeStamp.get()

        # TODO pagination
        r = tripit.get('https://api.tripit.com/v1/list/trip', params={'past': 'true',
            'modified_since': modified_since,
            'traveller': 'true',
            'page_size': 50})

        r.raise_for_status()
        past = r.json()
        trips = past.get('Trip', [])
        if not isinstance(trips, list):
            trips = [trips]

        r = tripit.get('https://api.tripit.com/v1/list/trip', params={'past': 'false',
            'modified_since': modified_since,
            'traveller': 'true',
            'page_size': 50})
        r.raise_for_status()
        future = r.json()
        trip_obj = future.get('Trip', [])

        # Tripit API only returns lists if there are plural objects >_<
        if isinstance(trip_obj, list):
            trips.extend(trip_obj)
        else:
            trips.append(trip_obj)

        if len(trips) == 0:
            self.stdout.write("No new trips found!")
            return 0

        for trip_obj in trips:
            self.stdout.write("Found trip {}".format(trip_obj['display_name']))
            trip, _ = Trip.objects.update_or_create(
                id=trip_obj['id'],
                defaults={'name': trip_obj['display_name']}
            )
            trip.segment_set.all().delete()
            trip.trainsegment_set.all().delete()
            for type_, obj, maker in [
                    ('air', 'AirObject', self._make_segment),
                    ('rail', 'RailObject', self._make_train_segment)]:
                segments = []
                r = tripit.get(
                    'https://api.tripit.com/v1/list/object/trip_id/'
                    '{}/type/{}'.format(trip.id, type_)
                )
                r.raise_for_status()
                objects = r.json().get(obj, [])

                # Tripit API only returns lists if there are plural objects >_<
                if not isinstance(objects, list):
                    objects = [objects]
                for mode_object in objects:
                    segment = mode_object['Segment']
                    if isinstance(segment, list):
                        segments.extend(segment)
                    else:
                        segments.append(segment)

                # Clear all segments so we can add new ones

                [maker(trip, segment) for segment in segments]

        TimeStamp.set(min(future['timestamp'], past['timestamp']))
