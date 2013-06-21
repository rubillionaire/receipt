# receipt/views.py
from datetime import datetime, timedelta
import logging

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (
    CreateView, UpdateView, DetailView)
from django.views.generic.base import View
from django.utils import simplejson

from braces.views import LoginRequiredMixin

from .models import Event
from .printer_mgmt import PrinterMgmt

receipt_printer = PrinterMgmt('Star_FVP10')

# get the weather every hour.
# if its older than an hour,
# don't include it on the receipt
## weather API endpoint
# http://api.wunderground.com/api/4be1df60aabd9d45/conditions/q/RI/Providence.json

# or do the weather in the browser
# using local storage to stash
# when it was last updated, and
# the latest value

logger = logging.getLogger(__name__)


class ReceiptEventView(View):
    template_name = 'receipt/event_base.html'

    # time objects for querying
    # past/present/future events
    # start with july 18th at 10am
    now = datetime.strptime('07 18 2013 10 00', '%m %d %Y %H %M')
    # now = datetime.now()

    def events(self, now):
        today = datetime.strptime(now.strftime('%m %d %y'), '%m %d %y')
        end_of_today = today + timedelta(hours=24)

        past_event = Event.objects.filter(start__gte=today,
                                          end__lt=now)\
                                  .order_by('start')

        present_event = Event.objects.filter(start__gte=today,
                                             start__lte=now,
                                             end__gte=now,
                                             end__lte=end_of_today)\
                                     .order_by('start')

        future_event = Event.objects.filter(start__gt=now,
                                            end__lte=end_of_today)\
                                    .order_by('start')

        future_events_count = Event.objects.filter(start__gt=now)\
            .count()

        # random future artists for footer
        random_future_events = Event.objects.filter(
            start__gt=end_of_today)\
            .order_by('start')[:2]

        random_future_artist_1 = random_future_events[0]\
            .artist.all()[0]
        random_future_artist_2 = random_future_events[1]\
            .artist.all()[0]
        # end random future artists for footer

        return past_event, present_event, future_event,\
            today, future_events_count, random_future_artist_1,\
            random_future_artist_2

    def get(self, request, time, *args, **kwargs):
        self.now = datetime.strptime(time, '%Y-%m-%dT%H-%M')
        past, present, future, today,\
            future_events_count,\
            random_future_artist_1,\
            random_future_artist_2 = self.events(self.now)

        return render(request, self.template_name, {
            'past_event': past,
            'present_event': present,
            'future_event': future,
            'future_events_count': future_events_count,
            'random_future_artist_1': random_future_artist_1,
            'random_future_artist_2': random_future_artist_2,
            'now': self.now,
            'today': today})


class ReceiptPrintView(ReceiptEventView):
    template_name = 'receipt/daily.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, {'now': self.now})


class ReceiptPrintDevView(ReceiptPrintView):
    template_name = 'receipt/daily_dev.html'


class QueueCheckView(View):
    def get(self, request, *args, **kwargs):
        print "\n\n---\nPrint Queue"
        print receipt_printer.queue
        print "---\n\n"
        status = {'print_status': 'being checked'}
        data = simplejson.dumps(status)
        return HttpResponse(data, mimetype='application/json')


class EventActionMixin(object):
    @property
    def action(self):
        msg = "{0} is missing action."
        msg = msg.format(self.__class__)
        raise NotImplementedError(msg)

    def form_valid(self, form):
        msg = "Event {0}"
        msg = msg.format(self.action)
        messages.info(self.request, msg)

        return super(EventActionMixin, self).form_valid(form)


class EventCreateView(LoginRequiredMixin, EventActionMixin, CreateView):
    model = Event
    action = "created"


class EventUpdateView(LoginRequiredMixin, EventActionMixin, UpdateView):
    model = Event
    action = "updated"


class EventDetailView(DetailView):
    model = Event
