from django.db import models

from model_utils import Choices
from model_utils.models import TimeFramedModel


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
        if self.pseudonym:
            return u'{0}'.format(self.pseudonym)
        else:
            return u'{0} {1}'.format(self.first_name, self.last_name)


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
        'Curator, Assembly',
        'Curator, Assembly + Artist Lab',
        'Demo + Discourse',
        'Office Hours',
        'Spotlight',
        'Spotlight with Franny',)
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
    def feature_name(self):
        artists = self.artist.all()
        if len(artists) > 1:
            return self.title
        else:
            return '{0} {1}'.format(artists[0].first_name, artists[0].last_name)

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
            artists_list = ', '.join([a.first_name for a in artists])
            return artists_list

    def __unicode__(self):
        if len(self.title) > 0:
            return u'{0}'.format(self.title)
        return u'No title'
