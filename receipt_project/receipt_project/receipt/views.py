# receipt/views.py
from datetime import datetime as dt

from django.views.generic.base import View
from django.shortcuts import render


class ReceiptPrintView(View):
    date = dt.now()
    template_name = 'receipt/daily.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'date': self.date})
