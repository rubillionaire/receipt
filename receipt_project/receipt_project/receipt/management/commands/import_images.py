from datetime import datetime as dt
from datetime import timedelta
import pytz
from subprocess import call
from os import walk
from os.path import abspath, dirname, join

import json
import time

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from ...models import Event, Artist


class ReceiptImages():
    """
    Setup data structure of images.
    """

    def __init__(self, filepath):
        self.filepath = filepath
        # reference to all images
        self.timezone = pytz.timezone('US/Eastern')
        self.images = self.read()

    def date(self, file):
        """
        make a datetime object for comparison against
        data in the db, to see which event each image
        belongs to.
        """
        date_str = file.split(" ")[0] + "_13"
        date = dt.strptime(date_str, '%m_%d_%y')
        datel = self.timezone.localize(date, is_dst=True)

        return datel

    def read(self):
        """read file directory for image names and file paths"""
        file_list = []
        for root, dirs, files in walk(self.filepath):
            if files:
                for f in files:
                    if (f.endswith('.jpg')) or (f.endswith('.JPG')):
                        image = {}
                        image['path'] = '{0}{1}'.format(self.filepath, f)
                        image['name'] = f
                        image['day'] = {}
                        image['day']['start'] = self.date(f)
                        image['day']['end'] = image['day']['start'] +\
                            timedelta(hours=24)
                        file_list.append(image)
        return file_list


class Command(BaseCommand):
    args = "No arguments."
    help = "Adds images to events based on file names."

    def process_image(self, event):
        directory = '/'.join(event.image.path.split('/')[0:-1])
        extension = event.image.path.split('.')[-1]

        resized_path = '{0}/resized.{1}'.format(directory, extension)
        halftone_path = '{0}/processed.{1}'.format(directory, extension)

        convert_image = 'convert {0} '.format(event.image.path) +\
                        '-resize 259x259^ ' +\
                        '{0}'.format(resized_path)

        halftone_image = 'convert ' +\
                             '{0} '.format(resized_path) +\
                             '-colorspace Gray -ordered-dither h4x4a ' +\
                             '{0}'.format(halftone_path)

        try:
            call(convert_image, shell=True)
            call(halftone_image, shell=True)
            print "computed!\n\n\n------"
        except:
            print "----------\n\n\n\ncan not compute!\n\n\n------"
        pass

    def handle(self, *args, **options):
        print "Reading in file paths."
        # get reference to images
        app_dir = dirname(abspath(__file__))
        filepath = '{0}/images_to_import/'.format(app_dir)
        images = ReceiptImages(filepath).images

        print "Matching events."
        # track matches and no matches
        no_match = []
        matches = []
        for img in images:
            try:
                events = Event.objects.filter(start__gte=img['day']['start'],
                                              end__lt=img['day']['end'])
                events_count = events.count()
                if events_count == 1:
                    event = events[0]
                elif events_count > 1:
                    found_match = False
                    for cur_event in events:
                        artists = cur_event.artist.all()
                        for artist in artists:
                            if artist.first_name.lower() in img['name'].lower() or\
                                    artist.last_name.lower() in img['name'].lower():
                                event = cur_event
                                found_match = True
                                # break from artist loop
                                break
                        if found_match:
                            # break from event loop
                            break
                    if not found_match:
                        no_match.append(img['name'])
                        print "skipped {0}".format(img['name'])
                        continue
                else:
                    no_match.append(img['name'])
                    print "skipped {0}".format(img['name'])
                    continue
                print img['path']
                with open(img['path'], 'r') as img_contents:
                    print event
                    event.image.save(img['name'], File(img_contents),
                                     save=True)

                event.save()
                matches.append({'name': img['path'], 'id': event.pk})
                print "{0}".format({'name': img['path'], 'id': event.pk})

                # process images
                self.process_image(event)
                # images are stored in directories
                # that are named by time. make sure
                # there is at least a second between
                # processing.
                time.sleep(1)

            except CommandError as detail:
                print "Error importing! {0}".format(detail)

        no_match_file = "{0}/images_to_import/".format(app_dir) +\
            "no_image_match-{0}.txt".format(dt.now().strftime('%Y-%m-%d'))

        with open(no_match_file, 'w') as documentation:
            documentation.write("\n".join(no_match))

        match_file = "{0}/images_to_import/".format(app_dir) +\
            "image-matches-{0}.txt".format(dt.now().strftime('%Y-%m-%d'))

        with open(match_file, 'w') as documentation:
            documentation.write(json.dumps(matches, separators=(',', ':')))

        success_msg = 'All images imported'
        self.stdout.write(success_msg)
