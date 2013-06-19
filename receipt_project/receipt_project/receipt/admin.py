from subprocess import call

from datetime import timedelta
from datetime import datetime

from django.contrib import admin

from .models import Event, Show, Artist


class EventAdmin(admin.ModelAdmin):
    ordering = ('start', )

    list_display = ('__unicode__', 'admin_artists', 'start',)
    readonly_fields = ('description', )

    fields = ('description', 'image', 'headline', 'title',
              'event_type','location', 'featured', 'artist',
              'start', 'end')

    def description(self, obj):
        four_hours = timedelta(hours=4)
        adjusted_end = obj.end - four_hours
        return '{0}: {1} in the {2} until about {3}.'.format(obj.event_type,
                                                             obj.title,
                                                             obj.location,
                                                             adjusted_end.strftime('%I%p')
                                                                .lstrip('0'))
    description.short_description = 'Description'

    def save_model(self, request, obj, form, change):
        new_image = request.FILES.get('image')
        obj.save()
        # resize and create half toned version
        # for display in the template
        if new_image:
            # print "\n\n\n\n----------"
            directory = '/'.join(obj.image.path.split('/')[0:-1])
            extension = obj.image.path.split('.')[-1]

            temp_path = '{0}/temp.{1}'.format(directory, extension)

            resized_path = '{0}/resized.{1}'.format(directory, extension)
            halftone_path = '{0}/processed.{1}'.format(directory, extension)

            convert_image = 'convert {0} '.format(obj.image.path) +\
                            '-resize 259x259^ ' +\
                            '{0}'.format(resized_path)
            # convert_image = convert_image.split(" ")
            # convert_image = shlex.split(convert_image)

            halftone_image = 'convert ' +\
                             '{0} '.format(resized_path) +\
                             '-colorspace Gray -ordered-dither h4x4a ' +\
                             '{0}'.format(halftone_path)
            # halftone_image = halftone_image.split(" ")
            # halftone_image = shlex.split(halftone_image)

            # print obj.image.path
            # print "\n\n"
            # print convert_image
            # print "\n\n"
            # print halftone_image
            # print "\n\n"

            # print "----------\n\n\n\n"

            try:
                call(convert_image, shell=True)
                call(halftone_image, shell=True)
                # print "computed!\n\n\n------"
            except:
                print "----------\n\n\n\ncan not compute!\n\n\n------"
            pass

admin.site.register(Event, EventAdmin)


class ShowAdmin(admin.ModelAdmin):
    pass

admin.site.register(Show, ShowAdmin)


class ArtistAdmin(admin.ModelAdmin):
    pass

admin.site.register(Artist, ArtistAdmin)