import codecs
from datetime import datetime as dt
from datetime import timedelta
import pytz
from os.path import abspath, dirname

from django.core.management.base import BaseCommand, CommandError

from ...models import Event, Artist


class ReceiptData():
    """
    Deal with Receipt Data
    """

    _default_schema = {
        "Event": {
            "featured": False,
            "location": 11,
            "event_type": 4,
            "title": 5,
            "date": 7,
            "start": 9,  # prepend date
            "end": 10,    # prepend date
        },
        "Artist": {
            "first_name": 2,
            "last_name": 1,
            "pseudonym": 3,
            "artist_type": False,
            "url": False,
            "twitterhandle": False,
            "image": False
        }

    }

    def __init__(self, filepath, schema=_default_schema):
        self.filepath = filepath

        # schema matches the models that will be made
        # based on the data in the tsv file.
        # Model attributes are keys, values are the
        # row index value for each item
        self.schema = schema

        self.data = self.import_from_file(self.filepath)

    """import data to be available to class"""
    def import_from_file(self, filepath):
        data = []
        with codecs.open(filepath, 'r', 'utf-8') as raw_data:
            count = 0
            for line in raw_data:
                count += 1
                if count == 1:
                    # first line is headings
                    continue

                # if count > 5:
                    # only wnat to read a couple for now
                    # break

                # raw data split into fields
                fields = line.split('\t')

                # create a datum for each line
                # basically mimics schema, but with
                # values instead of row indicies
                datum = {}
                for model in self.schema:
                    datum[model] = {}
                    for field in self.schema[model]:
                        if self.schema[model][field]:
                            datum[model][field] = fields[self.schema[model][field]].strip()
                        else:
                            datum[model][field] = ""
                data.append(datum)
        return data


class Command(BaseCommand):
    args = "No arguments."
    help = "Adds to database from TSV"

    # used to localize dates
    timezone = pytz.timezone('US/Eastern')

    def start_end(self, date, start, end, event_type):
        """returns a start and end datetime object"""
        if len(date) < 1:
            # no date, no datetime for both
            # start and end feilds
            return None, None

        date_str = u'{0}'.format(date)
        if start:
            start = self.format_time(start)
            start_str = u'{0} {1}'.format(date_str, start)
            start_dt = dt.strptime(start_str, '%m/%d/%y %I:%M%p')
            # localize it
            start_dtl = self.timezone.localize(start_dt, is_dst=True)

            if end:
                end = self.format_time(end)
                end_str = u'{0} {1}'.format(date_str, end)
                end_dt = dt.strptime(end_str, '%m/%d/%y %I:%M%p')
            else:
                if event_type == 'Office Hours':
                    end_dt = start_dt + timedelta(hours=2)
                else:
                    end_dt = start_dt + timedelta(hours=1)

            end_dtl = self.timezone.localize(end_dt, is_dst=True)

            return start_dtl, end_dtl

        else:
            # no start time, no end time. just a date
            return dt.strptime(date_str, '%m/%d/%y'),\
                dt.strptime(date_str, '%m/%d/%y')

    def format_time(self, time):
        """returns time with an m appended if necessary"""
        if time[-1] != 'm' and\
           time[-1] != 'M':
            time += 'm'

        return time

    def handle(self, *args, **options):
        app_dir = dirname(abspath(__file__))
        filepath = '{0}/data_to_import/data.tsv'.format(app_dir)
        receipt_data = ReceiptData(filepath).data
        for datum in receipt_data:
            try:
                # get the artist situated, so it can be
                # associated with the new event
                artist, created = Artist.objects.get_or_create(
                    first_name=datum['Artist']['first_name'],
                    last_name=datum['Artist']['last_name'])

                if created:
                    artist.pseudonym = datum['Artist']['pseudonym']
                    artist.artist_type = datum['Artist']['artist_type']
                    artist.url = datum['Artist']['url']
                    artist.twitterhandle = datum['Artist']['twitterhandle']
                    artist.image = datum['Artist']['image']

                start, end = self.start_end(datum['Event']['date'],
                                            datum['Event']['start'],
                                            datum['Event']['end'],
                                            datum['Event']['event_type'])

                event, ev_created = Event.objects.get_or_create(
                    location=datum['Event']['location'],
                    title=datum['Event']['title'],
                    start=start,
                    end=end)

                if ev_created:
                    event.event_type = datum['Event']['event_type']
                    event.featured = datum['Event']['featured']

                event.artist.add(artist)

                print event
                event.save()

            except CommandError as detail:
                print "Error importing! {0}".format(detail)

        success_msg = 'All data imported'
        self.stdout.write(success_msg)

