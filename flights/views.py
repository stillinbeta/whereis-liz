import logging

from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone


from flights.models import Segment, TrainSegment

logger = logging.getLogger('django')

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self):
        air_segment = Segment.objects.filter(start_time__lt=timezone.now()).latest('end_time')
        rail_segment = TrainSegment.objects.filter(start_time__lt=timezone.now()).latest('end_time')
        if air_segment.end_time > rail_segment.end_time:
            segment = air_segment
        else:
            segment = rail_segment

        logger.warning("most recent segment: " + str(segment))
        lat, lng = segment.end_ltlng.split(',')
        return {'city': segment.end_city,
                'lat': lat,
                'lng': lng}
