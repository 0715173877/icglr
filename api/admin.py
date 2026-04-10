from django.contrib import admin
from .models import Mine

@admin.register(Mine)
class MineAdmin(admin.ModelAdmin):
    list_display = ['mine_site_name', 'national_id', 'certification_status', 
                   'activity_status', 'admin1', 'admin2']
    list_filter = ['certification_status', 'activity_status', 'license_type', 'admin1']
    search_fields = ['mine_site_name', 'national_id', 'license_id']
    readonly_fields = ['created_at', 'updated_at']
