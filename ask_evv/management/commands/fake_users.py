from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ask_evv.models import Profile

from faker import Factory
import urllib.request
from PIL import Image
from io import BytesIO
import requests
from django.core.files import File


class Command(BaseCommand):
    help = 'Creates fake users'

    def add_arguments(self, parser):
        parser.add_argument('--number',
                            action='store',
                            dest='number',
                            default=10,
                            help='Number of users to add'
                            )

    def handle(self, *args, **options):
        fake = Factory.create()
        fakeru = Factory.create('ru_RU')

        number = int(options['number'])

        for i in range(0, number):
            profile = fake.simple_profile()

            u = User()
            u.username = profile['username']
            u.first_name = fakeru.first_name()
            u.last_name = fakeru.last_name()
            u.email = profile['mail']
            u.password = make_password('tp2015')
            u.is_active = True
            u.is_superuser = False
            u.save()

            up = Profile()
            up.user = u
            up.info = '%s (%s)' % (fakeru.company(), fakeru.company())

            image_url = 'http://api.adorable.io/avatars/100/%s.png'\
                        % u.username
            content = requests.get(image_url).content
            up.avatar.save('%s.png' % u.username,
                           File(BytesIO(content)), save=True)
            up.save()

            self.stdout.write('[%d] added user %s' % (u.id, u.username))
