from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, url

from .views import ReceiptPrintView, ReceiptEventView,\
                   QueueCheckView, ReceiptPrintDevView,\
                   ReceiptImageDevView

urlpatterns = patterns(
    '',
    url(
        r'^/?$',
        view=ReceiptPrintView.as_view(),
        name="receipt"
    ),
    url(
        r'^dev/?$',
        view=ReceiptPrintDevView.as_view(),
        name="receipt_dev"
    ),
    url(
        r'^dev/images/(?P<event_id>\d+)/?$',
        view=ReceiptImageDevView.as_view(),
        name="receipt_images"
    ),
    url(
        r'^events/(?P<time>[-\w]+)',
        view=ReceiptEventView.as_view(),
        name="receipt_event"
    ),
    url(
        r'^printed/?$',
        view=QueueCheckView.as_view(),
        name="queue_check"
    ),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
