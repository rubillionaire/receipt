from os.path import abspath, dirname

from django.core.management.base import BaseCommand, CommandError

from ....models import Event, Artist


class ReceiptData():
    """
    Dea with Receipt Data
    """

    _default_schema = {
        "Event": {
            "featured": False,
            "location": False,
            "event_type": 7,
            "title": 8,
            "date": 3,
            "start": 4,  # prepend date
            "end": 5,    # prepend date
        },
        "Artist": {
            "first_name": 1,
            "last_name": 2,
            "pseudonym": 6,
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
        with open(filepath, 'r') as raw_data:
            count = 0
            for line in raw_data:
                count += 1
                if count == 1:
                    # first line is headings
                    continue

                if count > 5:
                    # only wnat to read a couple for now
                    break

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
                            datum[model][field] = fields[self.schema[model][field]]
                data.append(datum)
        return data





class Command(BaseCommand):


if __name__ == '__main__':
    app_dir = dirname(abspath(__file__))
    filepath = '{0}/data_to_import/names_may31.tsv'.format(app_dir)
    receipt_data = ReceiptData(filepath)

