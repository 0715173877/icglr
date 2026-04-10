import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from api.models import GuidanceData

class Command(BaseCommand):
    help = 'Seeds the database with info from the dummy Excel file'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='Tanzania_Dummy_Data.xlsx')

    def handle(self, *args, **options):
        file_name = options['file']
        
        # Traverse up from base dir to find the file
        project_folder = settings.BASE_DIR.parent
        target_folder = project_folder.parent
        
        file_path = os.path.join(target_folder, file_name)
        if not os.path.exists(file_path):
            file_path = os.path.join(project_folder, file_name)
            
            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f"File {file_name} not found."))
                return

        self.stdout.write(f"Reading {file_path}...")
        df = pd.read_excel(file_path)
        
        # Clean NaNs
        df = df.where(pd.notnull(df), None)

        created_count = 0
        for index, row in df.iterrows():
            section = row.get('Section', '')
            orientation = row.get('Orientação', '')
            
            if section or orientation: # Only create if not fully empty
                GuidanceData.objects.create(
                    section=str(section) if section else "",
                    orientation=str(orientation) if orientation else ""
                )
                created_count += 1
                
        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {created_count} GuidanceData records from Excel!"))
