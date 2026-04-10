from django.db import models

class Mine(models.Model):
    CERTIFICATION_STATUS_CHOICES = [
        ('Blue', 'Blue'),
        ('Red', 'Red'),
        ('Green', 'Green'),
        ('Yellow', 'Yellow'),
    ]
    
    ACTIVITY_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Non-active', 'Non-active'),
    ]
    
    LICENSE_TYPE_CHOICES = [
        ('other', 'Other'),
        ('artisanal_permit', 'Artisanal Permit'),
        ('claim', 'Claim'),
        ('exploration_permit', 'Exploration Permit'),
        ('unlicensed', 'Unlicensed'),
        ('mining_license', 'Mining License'),
    ]
    
    mine_site_id = models.CharField(max_length=100, unique=True, db_index=True)
    mine_site_name = models.CharField(max_length=200, db_index=True)
    country_iso2 = models.CharField(max_length=2, default='TZ')
    national_id = models.CharField(max_length=50, db_index=True)
    certification_status = models.CharField(max_length=20, choices=CERTIFICATION_STATUS_CHOICES, db_index=True)
    activity_status = models.CharField(max_length=20, choices=ACTIVITY_STATUS_CHOICES, db_index=True)
    primary_mineral_hs_code = models.CharField(max_length=20, db_index=True)
    additional_minerals_hs_codes = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    polygon_geojson = models.TextField(blank=True, null=True)
    admin1 = models.CharField(max_length=50, db_index=True)
    admin2 = models.CharField(max_length=50, db_index=True)
    license_id = models.CharField(max_length=50, db_index=True)
    license_type = models.CharField(max_length=50, choices=LICENSE_TYPE_CHOICES, db_index=True)
    owner_company_id = models.CharField(max_length=50, db_index=True)
    operator_company_id = models.CharField(max_length=50, db_index=True)
    last_inspection_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['mine_site_name', 'certification_status']),
            models.Index(fields=['admin1', 'admin2']),
        ]
    
    def __str__(self):
        return f"{self.mine_site_name} ({self.national_id})"
