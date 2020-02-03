from .models import app_name
from rest_framework import serializers

class app_nameSerializer(serializers.ModelSerializer):
    class Meta:
        model = app_name
        fields = '__all__'