import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Automatically backs up the database to a JSON file'

    def handle(self, *args, **kwargs):
        # Create a timestamp for the backup filename
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f'backup_{now}.json'
        
        # Create a 'backups' folder if it doesn't exist
        backup_dir = os.path.join('backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Full path to the backup file
        backup_path = os.path.join(backup_dir, backup_filename)

        # Run Django's dumpdata command and save the backup
        with open(backup_path, 'w') as backup_file:
            call_command('dumpdata', stdout=backup_file)

        # Output a success message
        self.stdout.write(self.style.SUCCESS(f'Successfully backed up to {backup_filename}'))
