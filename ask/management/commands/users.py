from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ask.models import Profile
from faker import Factory
from django.core.files import File
import urllib


class Command(BaseCommand):
    help = 'Fill users'

    def add_arguments(self, parser):
        parser.add_argument('--number',
                            action='store',
                            dest='number',
                            default=10,
                            help='Number of users to add'
                            )

    def handle(self, *args, **options):
        fake = Factory.create()
        fakeen = Factory.create('en_US')

        number = int(options['number'])

        for i in range(0, number):
            profile = fake.simple_profile()

            u = User.objects.create_user(profile['username'], profile['mail'], make_password('qwerty'))
            u.first_name = fakeen.first_name()
            u.last_name = fakeen.last_name()
            u.is_active = True
            u.is_superuser = False
            u.save()

            up = Profile()
            up.user = u
            up.save()
