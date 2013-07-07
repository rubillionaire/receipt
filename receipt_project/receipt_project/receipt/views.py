# receipt/views.py
from datetime import datetime, timedelta
import pytz
import sys

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.utils import simplejson

from .models import Event, Weather
from .printer_mgmt import PrinterMgmt

receipt_printer = PrinterMgmt()

utc = pytz.UTC


class ReceiptEventView(View):
    template_name = 'receipt/event_base.html'
    pre_show_template_name = 'receipt/pre_show_event_base.html'

    # time objects for querying
    # past/present/future events
    # start with july 18th at 10am
    # now = datetime.strptime('07 18 2013 10 00', '%m %d %Y %H %M')
    now = datetime.now()

    def weather(self):
        last_hour = self.now + timedelta(hours=-1.5)

        # localize last hour
        last_hourl = utc.localize(last_hour)

        # get weather data
        data = Weather.objects.all()[0]

        # print >>sys.stderr, "\n\n---\n"
        # print >>sys.stderr, "{0}".format(last_hourl)
        # print >>sys.stderr, "{0}".format(data.updated)
        # print >>sys.stderr, "\n---\n\n"

        if data.updated > last_hourl:
            return data
        else:
            return ''

    def random_artists(self):
        # random future artists for footer
        random_future_events = Event.objects.filter(
            start__gt=self.end_of_today)\
            .order_by('start')[:2]

        random_future_artist_1 = random_future_events[0]\
            .artist.all()[0]
        random_future_artist_2 = random_future_events[1]\
            .artist.all()[0]
        # end random future artists for footer

        return random_future_artist_1,\
            random_future_artist_2

    def future_count(self):
        future_events_count = Event.objects.filter(start__gt=self.now)\
            .count()

        return future_events_count

    def events(self):
        past_event = Event.objects.filter(start__gte=self.today,
                                          end__lt=self.now)\
                                  .order_by('start')

        present_event = Event.objects.filter(start__gte=self.today,
                                             start__lte=self.now,
                                             end__gte=self.now,
                                             end__lte=self.end_of_today)\
                                     .order_by('start')

        future_event = Event.objects.filter(start__gt=self.now,
                                            end__lte=self.end_of_today)\
                                    .order_by('start')

        return past_event, present_event, future_event

    def get(self, request, time, *args, **kwargs):
        # set relavent times
        self.now = datetime.strptime(time, '%Y-%m-%dT%H-%M')
        self.today = datetime.strptime(
            self.now.strftime('%m %d %y'),
            '%m %d %y')
        self.end_of_today = self.today + timedelta(hours=24)

        # get weather from db
        current_temp = self.weather()

        # get start date to determine which
        # template to display. (teaser, or event data)
        show_start_date = datetime.strptime('2013-07-18',
                                            '%Y-%m-%d')

        # random future artists for the footer
        random_future_artist_1, random_future_artist_2 =\
            self.random_artists()

        # count of future events for the footer
        future_events_count = self.future_count()

        if self.now < show_start_date:
            # show hasn't started, render a teaser
            return render(
                request, self.pre_show_template_name, {
                    'now': self.now,
                    'temp': current_temp,
                    'future_events_count': future_events_count,
                    'random_future_artist_1': random_future_artist_1,
                    'random_future_artist_2': random_future_artist_2,
                })

        else:
            # show is on, give them a guide
            past, present, future = self.events()

            return render(request, self.template_name, {
                'past_event': past,
                'present_event': present,
                'future_event': future,
                'future_events_count': future_events_count,
                'random_future_artist_1': random_future_artist_1,
                'random_future_artist_2': random_future_artist_2,
                'now': self.now,
                'today': self.today,
                'temp': current_temp})


class ReceiptPrintView(ReceiptEventView):
    template_name = 'receipt/daily.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, {'now': self.now})


class ReceiptPrintDevView(ReceiptPrintView):
    template_name = 'receipt/daily_dev.html'


class ReceiptImageDevView(View):
    """test out images"""
    images = ["processed.jpg",
              "processed_h4x4o.jpg",
              "processed_h6x6a.jpg",
              "processed_2x1.jpg",
              "processed_h6x6o.jpg",
              "processed_2x2.jpg",
              "processed_h8x8a.jpg",
              "processed_3x3.jpg",
              "processed_h8x8o.jpg",
              "processed_4x1.jpg",
              "processed_moreoffsethalftone.jpg",
              "processed_4x4.jpg",
              "processed_o2x2.jpg",
              "processed_6x1.jpg",
              "processed_o3x3.jpg",
              "processed_8x1.jpg",
              "processed_o4x4.jpg",
              "processed_8x8.jpg",
              "processed_o8x8.jpg",
              "processed_checks.jpg",
              "processed_offsethalftone.jpg",
              "processed_h16x16o.jpg",
              "processed_threshold.jpg",
              "processed_h4x4a.jpg"]
    images.sort()

    # ids that are set up.
    # [22, 136, 71]

    template_name = 'receipt/image_dev.html'

    def get(self, request, event_id):

        event = Event.objects.get(pk=event_id)

        return render(request, self.template_name,
                      {'event': event,
                       'images': self.images})

class QueueCheckView(View):
    def get(self, request, *args, **kwargs):
        print "\n\n---\nPrint Queue"
        status = receipt_printer.check()
        print "---\n\n"
        data = simplejson.dumps(status)
        return HttpResponse(data, mimetype='application/json')
