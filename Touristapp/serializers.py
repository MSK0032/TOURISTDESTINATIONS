from rest_framework import serializers
from .models import TouristDestination

class TouristDestinationSerializer(serializers.ModelSerializer):
    tourist_img = serializers.ImageField(required=False)

    class Meta:
        model = TouristDestination
        fields = '__all__'
