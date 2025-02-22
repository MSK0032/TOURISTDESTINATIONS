from rest_framework import serializers
from .models import TouristDestination,CustomUser

class TouristDestinationSerializer(serializers.ModelSerializer):
    tourist_img = serializers.ImageField(required=False)

    class Meta:
        model = TouristDestination
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_admin']