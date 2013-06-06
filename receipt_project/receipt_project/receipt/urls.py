from django.conf.urls import patterns, url

from .views import ReceiptPrintView

urlpatterns = patterns(
    '',
    url(
        r'^/?$',
        view=ReceiptPrintView.as_view(),
        name="receipt"
    ),
)
