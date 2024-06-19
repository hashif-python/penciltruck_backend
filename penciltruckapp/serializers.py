from rest_framework import serializers
from penciltruckadmin.models import Gallery
from django.conf import settings

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
