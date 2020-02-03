from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import pickle
from django.conf import settings
import os
from media_handling.views import authorization
from media_handling.models import app_name
from media_handling.serializers import app_nameSerializer

class evaluateModel(APIView):
    def get(self, request,app):
        check = authorization(request)
        if check:
            return check
        url = 'http://127.0.0.1:8000/api/model/'+ app
        print(url)
        queryset = app_name.objects.filter(url=url)
        model_file_name = queryset[0]['model_file']
        toml_file_name = queryset[0]['toml_file']
        
        root1 = 'modelFiles/'+model_file_name
        root2 = 'TOML_Files/'+toml_file_name

        file_name = os.path.join(settings.MEDIA_ROOT,root1)
        with open(file_name, 'rb') as f:
            data = pickle.load(f)
            data.predict()  
        
        Response.status_code = 200

        return Response("")
    
