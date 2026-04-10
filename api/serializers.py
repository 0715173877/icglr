from rest_framework import serializers
from .models import Mine

class MineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mine
        exclude = ['id', 'last_inspection_date', 'notes', 'created_at', 'updated_at']
    
    def validate_latitude(self, value):
        if value and (value < -90 or value > 90):
            raise serializers.ValidationError("Latitude must be between -90 and 90")
        return value
    
    def validate_longitude(self, value):
        if value and (value < -180 or value > 180):
            raise serializers.ValidationError("Longitude must be between -180 and 180")
        return value

class MineListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    class Meta:
        model = Mine
        fields = ['mine_site_id', 'mine_site_name', 'certification_status', 
                  'activity_status', 'admin1', 'admin2', 'latitude', 'longitude']
