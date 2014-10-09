from django.test import TestCase

from flights.models import TimeStamp

# Create your tests here.
class TimestampTest(TestCase):
    def test_timestamp(self):
        val = 1410678000

        TimeStamp.set(val)
        self.assertEqual(val, TimeStamp.get())
