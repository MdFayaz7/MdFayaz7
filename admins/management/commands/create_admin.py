from django.core.management.base import BaseCommand
from admins.models import Admin
import uuid

class Command(BaseCommand):
    help = 'Create a default admin user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Admin username (default: admin)'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Admin password (default: admin123)'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@college.com',
            help='Admin email (default: admin@college.com)'
        )

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']
        
        # Check if admin already exists
        if Admin.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Admin with username "{username}" already exists.')
            )
            return
        
        # Create admin user
        admin = Admin(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            full_name='System Administrator',
            is_active=True,
            is_super_admin=True
        )
        admin.set_password(password)
        admin.save()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created admin user:\n'
                f'Username: {username}\n'
                f'Password: {password}\n'
                f'Email: {email}'
            )
        )
