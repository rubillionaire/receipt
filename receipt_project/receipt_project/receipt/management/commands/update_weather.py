# get the weather every hour.
# if its older than an hour,
# don't include it on the receipt

import pytz
import requests

from django.core.management.base import BaseCommand, CommandError

from ...models import Weather


class WeatherUpdater():
    def __init__(self):
        ## weather API endpoint
        self.url = 'http://api.wunderground.com/' +\
            'api/4be1df60aabd9d45/conditions/q/RI/Providence.json'

    def update(self):
        r = requests.get(self.url)
        return r.json()

    def update_test(self):
        import json
        test_file = '/Users/risdworks/Documents/receipt_env/' +\
            'repo/receipt/receipt_project/receipt_project/' +\
            'receipt/management/commands/test_weather_data/' +\
            'Providence.json'
        with open(test_file, 'rb') as r:
            weather_dict = json.loads(r.read())
        return weather_dict


class Command(BaseCommand):
    args = "No arguments."
    help = "Adds to database from TSV"

    timezone = pytz.timezone('US/Eastern')

    def handle(self, *args, **options):
        updater = WeatherUpdater()
        weather_data = updater.update()

        try:
            # get weather model to update
            weather_count = Weather.objects.all().count()
            if weather_count == 0:
                weather_tracker = Weather()
            else:
                weather_tracker = Weather.objects.all()[0]

            # update the model
            weather_tracker.temp_f = \
                weather_data['current_observation']['temp_f']

            weather_tracker.temp_c = \
                weather_data['current_observation']['temp_c']

            weather_tracker.temp_str = \
                weather_data['current_observation']['temperature_string']

            weather_tracker.weather = \
                weather_data['current_observation']['weather']

            weather_tracker.save()

        except CommandError as detail:
            print "error getting weather model to update! " +\
                "{0}".format(detail)

        success_msg = 'Weather has been updated.'
        self.stdout.write(success_msg)
