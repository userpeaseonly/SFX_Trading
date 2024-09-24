# users/management/commands/createsuperuserifnone.py
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
import os

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            admin_phone_number = os.environ.get('ADMIN_PHONE_NUMBER')
            admin_password = os.environ.get('ADMIN_PASSWORD', 'yourpassword')
            admin_telegram_id = os.environ.get('ADMIN_TELEGRAM_ID', 'admin_telegram_id')
            if admin_phone_number:
                self.stdout.write(self.style.SUCCESS('No superuser found. Creating one...'))
                User.objects.create_superuser(
                    phone_number=admin_phone_number,
                    password=admin_password,
                    telegram_id=admin_telegram_id
                )
            else:
                self.stdout.write(self.style.ERROR('ADMIN_PHONE_NUMBER not set in environment variables.'))
        else:
            self.stdout.write(self.style.WARNING('A superuser already exists.'))
