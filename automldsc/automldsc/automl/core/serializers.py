from .models import Core_Model
from rest_framework import serializers

class CoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Core_Model
        fields = '__all__'