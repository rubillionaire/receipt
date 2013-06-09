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


class Event(TimeFramedModel):
    featured = models.BooleanField(
        default=False,
        blank=False,
        null=False)

    artist = models.ForeignKey(
        'Artist',
        blank=True)

    GALLERIES = Choices(
        'Lower Farago',
        'Spalter New Media',
        'Upper Farago')
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

    def __unicode__(self):
        return u'{0}'.format(self.title)

    # Description box that will override the use of
    # a data driven description


class Artist(models.Model):
    first_name = models.CharField(max_length=255, null=False, blank=True)
    last_name = models.CharField(max_length=255, null=False, blank=True)
    pseudonym = models.CharField(max_length=255, null=False, blank=True)

    artist_type = models.CharField(max_length=255, null=False, blank=True)

    url = models.CharField(max_length=255, null=False, blank=True)
    twitterhandle = models.CharField(max_length=255, null=False, blank=True)
    ## if image magick
    image = models.FileField(upload_to="artists/%Y-%m-%d/%M-%S")
    ## if pil
    # image = models.ImageField(upload_to="artists/%Y-%m-%d/%M-%S")

    def __unicode__(self):
        if self.pseudonym:
            return u'{0}'.format(self.pseudonym)
        else:
            return u'{0} {1}'.format(self.first_name, self.last_name)
