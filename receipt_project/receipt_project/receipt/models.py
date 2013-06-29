from datetime import datetime
import pytz

from django.db import models

from model_utils import Choices
from model_utils.models import TimeFramedModel


timezone = pytz.timezone('US/Eastern')


# At {{ 9am }}, this {{ morning }},
# {{ professor and architect}},
# {{ Brian Goldberg }} {{ is holding
# Office Hours - an open format where
# you can talk with experts }}


class Show(models.Model):
    title = models.CharField(
        max_length=255,
        default="Locally Made",
        null=False)

    default_info = "runs through November 3rd, 2013. " +\
                   "There are 130 more performances and " +\
                   "programs from local artists including " +\
                   "Peter Glantz and Meredith Stern."
    info = models.TextField(
        default=default_info,
        null=False)

    def __unicode__(self):
        return u'{0}'.format(self.title)


class Artist(models.Model):
    first_name = models.CharField(max_length=255, null=False, blank=True)
    last_name = models.CharField(max_length=255, null=False, blank=True)
    pseudonym = models.CharField(max_length=255, null=False, blank=True)

    artist_type = models.CharField(max_length=255, null=False, blank=True)

    url = models.CharField(max_length=255, null=False, blank=True)
    twitterhandle = models.CharField(max_length=255, null=False, blank=True)

    def __unicode__(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)

    class Meta:
        ordering = ['first_name']


class Event(TimeFramedModel):

    featured = models.BooleanField(
        default=False,
        blank=False,
        null=False)

    artist = models.ManyToManyField(
        Artist,
        blank=True)

    GALLERIES = Choices(
        'Lower Farago Gallery',
        'Spalter New Media Gallery',
        'Fain Gallery',
        'Upper Farago Gallery')
    location = models.CharField(
        max_length="255",
        choices=GALLERIES,
        default="",
        null=False,
        blank=True)

    TYPES = Choices(
        'Assembled',
        'Artist Lab',
        'Demo + Discourse',
        'Office Hours',
        'Spotlight',)
    event_type = models.CharField(
        max_length="255",
        choices=TYPES,
        default="",
        null=False,
        blank=True,
        verbose_name="Format")

    title = models.CharField(
        max_length=255,
        null=False,
        blank=True)

    headline = models.CharField(
        max_length=255,
        null=False,
        blank=True)

    notes = models.TextField(
        default='',
        null=False,
        blank=True)

    image = models.FileField(upload_to="events/%Y-%m-%d/%H-%M-%S",
                             null=True,
                             blank=True)

    def processed_image(self):
        directory = '/'.join(self.image.url.split('/')[0:-1])
        extension = self.image.url.split('.')[-1]
        return '{0}/processed.{1}'.format(directory, extension)

    # media directory for event images
    def media_directory(self):
        directory = '/'.join(self.image.url.split('/')[0:-1])
        return directory

    def location_description(self):
        location_map = {
            'Lower Farago Gallery': u'here',
            'Fain Gallery': u'around the corner'
        }

        if self.location in location_map:
            return location_map[self.location]
        else:
            return u'not-in-database'

    def admin_artists(self):
        return ', '.join([a.first_name for a in self.artist.all()])
    admin_artists.short_description = "Artists"

    # used for the large text
    # associated with each event
    def template_headline(self):

        hl = self.headline.strip()

        # check for shorties.
        if len(hl) <= 10:
            # check for image
            if self.image:
                return hl
            else:
                # if no image, make one line
                return hl.replace(' ', '&nbsp;')

        # check for short parts that can be on
        # the same line as their preceding line
        hl_split = hl.split(" ")
        if len(hl_split) >= 3:
            first_two = len(hl_split[0]) + len(hl_split[1])
            if first_two <= 9:
                first_two = '{0}&nbsp;{1}'.format(hl_split[0],
                                                  hl_split[1])
                return '{0} {1}'.format(first_two,
                                        ' '.join(hl_split[2:]))

        # check for long parts
        make_smaller = False
        for piece in hl_split:
            if len(piece) > 10:
                make_smaller = True

        if make_smaller:
            return '<span class="smaller">{0}</span>'.format(hl)

        return hl

    # used for the last sentence
    # in the description
    def more_on(self):
        artists = self.artist.all()
        if len(artists) == 1:
            if artists[0].url:
                return 'More on {0} at {1}.'.format(artists[0].first_name,
                                                    artists[0].url)
            else:
                return ''
        else:
            artists_list = ', '.join([a.first_name + " " + a.last_name \
                                      for a in artists])
            return 'Includes {0}.'.format(artists_list)


    def more_on_past(self):
        artists = self.artist.all()
        if len(artists) == 1:
            if artists[0].url:
                return 'More on {0} at {1}.'.format(artists[0].first_name,
                                                    artists[0].url)
            else:
                return ''
        else:
            artists_list = ', '.join([a.first_name + " " + a.last_name \
                                      for a in artists])
            return 'Included {0}.'.format(artists_list)

    def __unicode__(self):
        if len(self.title) > 0:
            return u'{0}'.format(self.title)
        return u'No title'
