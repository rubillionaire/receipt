from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, url

from .views import ReceiptPrintView, ReceiptEventView

urlpatterns = patterns(
    '',
    url(
        r'^/?$',
        view=ReceiptPrintView.as_view(),
        name="receipt"
    ),
    url(
        r'^events/(?P<time>[-\w]+)',
        view=ReceiptEventView.as_view(),
        name="receipt_event"
    ),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
