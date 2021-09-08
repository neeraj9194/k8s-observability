from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Addes a superuser if not exists already'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username of admin user')
        parser.add_argument('--password', type=str, help='Password of admin user')

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = options['username']
            password = options['password']
            print(f'Creating account for {username}')
            User.objects.create_superuser(username=username, password=password)
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
