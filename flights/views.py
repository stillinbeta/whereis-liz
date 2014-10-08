from datetime import datetime

from django.shortcuts import render
from django.views.generic import TemplateView

from flights.models import Segment

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self):
        segment = Segment.objects.filter(start_time__lt=datetime.now()).latest('start_time')
        lat, lng = segment.end_ltlng.split(',')
        return {'city': segment.end_city,
                'lat': lat,
                'lng': lng}
