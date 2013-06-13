from django.db import models
from modelutils.models import TimeFrameModel

Show
    title = models.CharField(max_length=255, default="Locally Made", null=False)

    default_info = "runs through November 3rd, 2013. " +\
                    "There are 130 more performances and "+\
                    "programs from local artists including " +\
                    "Peter Glantz and Meredith Stern."
    info = models.TextField(default=default_info null=False) 


class Event(TimeFrameModel)
    featured = models.BooleanField(default=False, blank=False, null=False)
    artist = models.ForeignKey('Artist', blank=True)
    location:options
        Lower Farago
        Upper Farago


Artist
    first_name = models.CharField(max_length=255, null=False, blank=True)
    last_name = models.CharField(max_length=255, null=False, blank=True)
    artist_type = models.CharField(max_length=255, null=False, blank=True)
    url = models.CharField(max_length=255, null=False, blank=True)
    twitterhandle = models.CharField(max_length=255, null=False, blank=True)
    image

ie
    Anna Galloway Highsmith
    ceramicist
    name@name.com
    twitter


At {{ 9am }}, this {{ morning }},
{{ professor and architect}},
{{ Brian Goldberg }} {{ is holding
Office Hours - an open format where
you can talk with experts }}




Is the image on the receipt something that is per Event, or per Artist?
    Should the same picture be used for all instances of Anna Galloway Highsmith?


Coming up at {{ 1pm }}, {{ take
part in Artist's Lab }} with
{{ ceramicist }} {{ Anna Galloway
Highsmith }}


Items at the bottom of the receipt that do not have.