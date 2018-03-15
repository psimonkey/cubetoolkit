# https://docs.djangoproject.com/en/1.11/howto/custom-management-commands/

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from toolkit.members.models import Member


class Command(BaseCommand):
    help = "Delete non-members who don't get the members mailout"

    def handle(self, *args, **options):

        dead_wood = (Member.objects.filter(email__isnull=False)
                                   .exclude(email='')
                                   .exclude(mailout_failed=True)
                                   .exclude(mailout=True)
                                   .exclude(is_member=True)
                     )

        self.stdout.write('Deleting...')

        for member in dead_wood:
            self.stdout.write('%s <%s> joined %s' % (
                member.name,
                member.email,
                member.created_at)
            )
        # member.delete()

        self.stdout.write(self.style.SUCCESS(
            '\nDeleted %d non-members\n' % len(dead_wood)))
