from django.core.management.base import BaseCommand, CommandError

from ...models import Event, Artist


class Command(BaseCommand):
    args = "No arguments."
    help = "Prepopulates headlines with artist names."

    def handle(self, *args, **options):
        events = Event.objects.all()
        for event in events:
            try:
                artists = event.artist.all()
                if artists:
                    if artists[0].pseudonym:
                        event.headline = "{0}".format(artists[0].pseudonym)
                    else:
                        event.headline = "{0} {1}".format(
                            artists[0].first_name,
                            artists[0].last_name)
                    event.save()
                else:
                    continue

            except CommandError as detail:
                print "Error copying! {0}".format(detail)

        success_msg = 'All data copied over.'
        self.stdout.write(success_msg)
