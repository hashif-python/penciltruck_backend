from rest_framework import serializers
from penciltruckadmin.models import Gallery,VolunteerRequest
from django.conf import settings
from .models import StudyMaterialDonation


class GallerySerializer(serializers.ModelSerializer):
    image1 = serializers.SerializerMethodField()
    image2 = serializers.SerializerMethodField()
    image3 = serializers.SerializerMethodField()
    image4 = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = '__all__'
        
    def get_image_url(self, image_field):
        if image_field:
            return f"{settings.HOST_URL}{image_field.url}"
        return None

    def get_image1(self, obj):
        return self.get_image_url(obj.image1)
    
    def get_image2(self, obj):
        return self.get_image_url(obj.image2)
    
    def get_image3(self, obj):
        return self.get_image_url(obj.image3)
    
    def get_image4(self, obj):
        return self.get_image_url(obj.image4)




class VolunteerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerRequest
        fields = ['name', 'email', 'phone', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

    def create(self, validated_data):
        # Automatically set status to 'Pending' and created_at to current time
        validated_data['status'] = 'Pending'
        return VolunteerRequest.objects.create(**validated_data)
    
    
class StudyMaterialDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterialDonation
        fields = '__all__'  # You can specify the fields explicitly if needed