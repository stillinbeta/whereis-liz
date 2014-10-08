import re
from datetime import datetime
from pprint import pprint
import os

from requests_oauthlib import OAuth1Session
from django.core.management.base import BaseCommand

from flights.models import Trip, Segment

class Command(BaseCommand):
    def _get_datetime(self, date_obj):
        return datetime.strptime(
            '{} {} {}'.format(date_obj['date'],
                              date_obj['time'],
                              date_obj['utc_offset'].replace(':', '')),
            '%Y-%m-%d %H:%M:%S %z'
        )

    def _get_duration(self, duration):
        match = re.match('(?:(\d+)h, )?(\d+)m', duration)
        if match is None:
            raise ValueError("Can't parse duration " + duration)
        hrs, mins = match.groups()
        if hrs is None:
            return int(mins)
        return int(hrs) * 60 + int(mins)

    def _get_distance(self, distance):
        match = re.match('([\d,]+) (\w+)', distance)
        if match is None:
            raise ValueError("Can't parse distance " + distance)
        distance, units = match.groups()
        distance = int(distance.replace(',',''))
        if units == 'miles':
            return distance
        elif units == 'km':
            return round(distance * 0.621)
        else:
            raise ValueError("Can't parse distance unit" + units)

    def handle(self, *args, **kwargs):
        tripit = OAuth1Session(
                os.environ['TRIPIT_OAUTH_KEY'],
                client_secret=os.environ['TRIPIT_OAUTH_SECRET'],
                resource_owner_key=os.environ['TRIPIT_CONSUMER_KEY'],
                resource_owner_secret=os.environ['TRIPIT_CONSUMER_SECRET'],
                )
        tripit.params.update({'format': 'json'})

        # TODO pagination
        r = tripit.get('https://api.tripit.com/v1/list/trip', params={'past': 'true',
            'traveller': 'true',
            'page_size': 50})

        r.raise_for_status()
        dict_ = r.json()
        trips = dict_['Trip']

        r = tripit.get('https://api.tripit.com/v1/list/trip', params={'past': 'false',
            'traveller': 'true',
            'page_size': 50})
        r.raise_for_status()
        trips.extend(r.json()['Trip'])

        for trip_obj in trips:
            flights = []
            trip, _ = Trip.objects.update_or_create(
                id=trip_obj['id'],
                defaults={'name': trip_obj['display_name']}
            )
            r = tripit.get('https://api.tripit.com/v1/list/object/trip_id/{}/type/air'.format(trip.id))
            r.raise_for_status()
            ao = r.json()['AirObject']
            if not isinstance(ao, list):
                ao = [ao]
            for res in ao:
                segment = res['Segment']
                if isinstance(segment, list):
                    flights.extend(segment)
                else:
                    flights.append(segment)
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
                    'distance_miles': self._get_distance(flight['distance']),
                    'duration_mins': self._get_duration(flight['duration']),
                }
                Segment.objects.update_or_create(id=flight['id'], defaults=segment)


