from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Crea un superusuario automáticamente si no existe'

    def handle(self, *args, **kwargs):
        username = os.getenv('ADMIN_USERNAME', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'admin@admin.com')
        password = os.getenv('ADMIN_PASSWORD', 'admin123456')
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'✅ Superusuario "{username}" creado con éxito'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️ El usuario "{username}" ya existe'))