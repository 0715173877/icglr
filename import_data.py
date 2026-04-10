import pandas as pd
import os
import django

# Corrected module path to match your actual project namespace
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mines_api_project.settings')
django.setup()

# Corrected the app path from mines.models to api.models
from api.models import Mine

def import_excel_data(file_path):
    # Read Excel file
    df = pd.read_excel(file_path, sheet_name='Mines')
    
    # Replace NaN with None
    df = df.where(pd.notnull(df), None)
    
    imported = 0
    skipped = 0
    
    for _, row in df.iterrows():
        try:
            mine, created = Mine.objects.update_or_create(
                mine_site_id=row['mine_site_id'],
                defaults={
                    'mine_site_name': row['mine_site_name'],
                    'country_iso2': row['country_iso2'],
                    'national_id': row['national_id'],
                    'certification_status': row['certification_status'],
                    'activity_status': row['activity_status'],
                    'primary_mineral_hs_code': row['primary_mineral_hs_code'],
                    'additional_minerals_hs_codes': row.get('additional_minerals_hs_codes'),
                    'latitude': row.get('latitude'),
                    'longitude': row.get('longitude'),
                    'polygon_geojson': row.get('polygon_geojson'),
                    'admin1': row.get('admin1'),
                    'admin2': row.get('admin2'),
                    'license_id': row.get('license_id'),
                    'license_type': row.get('license_type'),
                    'owner_company_id': row.get('owner_company_id'),
                    'operator_company_id': row.get('operator_company_id'),
                    'last_inspection_date': row.get('last_inspection_date'),
                    'notes': row.get('notes'),
                }
            )
            imported += 1
            print(f"{'Created' if created else 'Updated'}: {mine.mine_site_name}")
        except Exception as e:
            skipped += 1
            print(f"Error importing {row.get('mine_site_name', 'Unknown')}: {e}")
    
    print(f"\nImport completed! Imported: {imported}, Skipped: {skipped}")

if __name__ == "__main__":
    import_excel_data('TZ_Mines.xlsx')
