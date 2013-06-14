from django.contrib import admin

from .models import Event, Show, Artist


class EventAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'admin_artists',)
    readonly_fields = ('description', )

    def description(self, obj):
        return '{0}: {1} in the {2} until about {3}.'.format(obj.event_type,
                                                             obj.title,
                                                             obj.location,
                                                             obj.end.strftime('%I%p'))
    description.short_description = 'Description'

admin.site.register(Event, EventAdmin)


class ShowAdmin(admin.ModelAdmin):
    pass

admin.site.register(Show, ShowAdmin)


class ArtistAdmin(admin.ModelAdmin):
    pass

admin.site.register(Artist, ArtistAdmin)