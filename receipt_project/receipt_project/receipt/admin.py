from django.contrib import admin

from .models import Event, Show, Artist


class EventAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'admin_artists',)

admin.site.register(Event, EventAdmin)


class ShowAdmin(admin.ModelAdmin):
    pass

admin.site.register(Show, ShowAdmin)


class ArtistAdmin(admin.ModelAdmin):
    pass

admin.site.register(Artist, ArtistAdmin)
