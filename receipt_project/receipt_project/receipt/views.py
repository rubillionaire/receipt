# receipt/views.py
from datetime import datetime as dt

from django.contrib import messages
from django.shortcuts import render
from django.views.generic import (
    CreateView, UpdateView, DetailView)
from django.views.generic.base import View

from braces.views import LoginRequiredMixin

from .models import Event


class ReceiptPrintView(View):
    date = dt.now()
    template_name = 'receipt/daily.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'date': self.date})


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