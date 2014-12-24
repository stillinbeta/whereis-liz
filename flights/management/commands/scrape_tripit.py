import re
from datetime import datetime
from pprint import pprint
import os

from django.core.management.base import BaseCommand
from requests_oauthlib import OAuth1Session

from flights.models import Trip, Segment, TimeStamp

class Command(BaseCommand):
    # fffffff
    DURATION_REGEXS = [
        r'(?:(\d+) hours)? (\d+) minutes',
        r'(?:(\d+)h, )?(\d+)m',
        r'(\d+):(\d+)',
    ]

    def _get_datetime(self, date_obj):
        return datetime.strptime(
            '{} {} {}'.format(date_obj['date'],
                              date_obj['time'],
                              date_obj['utc_offset'].replace(':', '')),
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
            flights = []
            trip, _ = Trip.objects.update_or_create(
                id=trip_obj['id'],
                defaults={'name': trip_obj['display_name']}
            )
            r = tripit.get('https://api.tripit.com/v1/list/object/trip_id/{}/type/air'.format(trip.id))
            r.raise_for_status()
            ao = r.json().get('AirObject', [])

            # Tripit API only returns lists if there are plural objects >_<
            if not isinstance(ao, list):
                ao = [ao]
            for res in ao:
                segment = res['Segment']
                if isinstance(segment, list):
                    flights.extend(segment)
                else:
                    flights.append(segment)

            # Clear all segments so we can add new ones
            trip.segment_set.all().delete()

            for flight in flights:
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

        TimeStamp.set(min(future['timestamp'], past['timestamp']))


