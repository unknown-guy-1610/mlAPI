from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import pickle

from .models import app_name
from .serializers import app_nameSerializer


def authorization(request):
    if 'Authorization' not in request.headers:
        Response.status_code = 403
        return Response({"status": "blocked", 
                        "message": "Authentication credentials not provided"
                        })
# Create your views here.
class CreatNewApp(APIView):

    
    def post(self, request):
        check = authorization(request)
        if check:
            return check
        app = request.data['app']
        request.data['url']= 'http://127.0.0.1:8000/api/model/'+ app
        request.data['user'] = str(request.user.id)
        print(request.data)
        serializer = app_nameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            Response.status_code = 201
            return Response(serializer.data)
        return Response(serializer.errors)




