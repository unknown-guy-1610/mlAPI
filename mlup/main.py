import os
import subprocess
from shutil import copyfile
import shutil
import toml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def excute(cmd):
    process = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)
    out, err = process.communicate()
    errcode = process.returncode
    return out,errcode

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def init(current_dir):
    shutil.move('.dsc.toml',current_dir)


def main(current_dir):
    
    print("Welcome to AutoML\n")
    current_dir+='.dsc.toml'
    toml_list = toml.load(current_dir)
    project_name = toml_list['project_name']
    print("Making project : ",project_name)
    input_dict = []
    excute('mkdir '+project_name)
    copytree('automl',project_name+'/')
    print("\n")
    input_text=''
    for i in toml_list['inputs']:
        feild_name = i['input_name']
        feild_type = i['input_type']
        
        if feild_type == 1: 
            input_text = feild_name+','
            max_length = i['max_length']
            input_dict.append('    '+ feild_name+' = models.CharField(max_length='+str(max_length)+')\n')
        elif feild_type==2:
            input_text = feild_name+','
            input_dict.append('    '+ feild_name +' = models.IntegerField()\n')
        elif feild_type==3:
            input_text = feild_name+','
            input_dict.append('    '+ feild_name +' = models.ImageField()\n')
        elif feild_type == 4:
            input_text = feild_name+','
            input_dict.append('    '+ feild_name +' = models.TextField()\n')
        
        else:
            print('Not a valid option exiting!')
            exit(0)
    output_list = toml_list['outputs']
    model_text = '''
    from django.db import models

    class Core_Model(models.Model):
        created = models.DateTimeField(auto_now_add=True)
    '''

    for i in input_dict:
        model_text+=i

    f = open('models.py',"a")
    f.write(model_text)
    f.close()
    shutil.move('models.py', project_name+'/core')
    views_text = '''

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

    main_string = '            '
    for i in toml_list['outputs']:
        main_string+=i['name']+','

    main_string = main_string[:-1] +'=predict(**input_arg)'
    views_text+=main_string
    bottom_views = '''
                
                Response.status_code = 201
                return Response(JSON_response)

            Response.status_code = 400
            return Response(serializer.errors)


    '''
    views_text+=bottom_views
    f = open('views.py',"a")
    f.write(views_text)
    f.close()
    shutil.move('views.py', project_name+'/core')
    print('Done')
    copytree(project_name+'/',current_dir)
    return True


def cli():
    option=input("Choose a option :\n 1) Create a init file\n 2)Create a project")
    if option==1:
        loc = input("Please paste the directory to generate init file :")
        init(loc)
    elif option==2:
        loc = input("Please paste the directory of .dsc.toml file :")
        main(loc)
    else:
        print("wrong option")