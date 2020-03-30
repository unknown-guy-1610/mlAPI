
VIEWS_BOTTOM = '''
            
            Response.status_code = 201
            return Response(serializer.data)

        Response.status_code = 400
        return Response(serializer.errors)


'''

MODEL_TEXT = '''
from django.db import models

class Core_Model(models.Model):
    created = models.DateTimeField(auto_now_add=True)
'''


VIEWS_TEXT = '''

from django.shortcuts import render
from .serializers import CoreSerializer
from .models import Core_Model
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .predicter import predict
from rest_framework.response import Response

class User_Add(APIView):

    def post(self,request):
        serializer = CoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            input_arg = request.data
'''