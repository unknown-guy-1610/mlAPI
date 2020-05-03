import os
import subprocess
from shutil import copyfile
import shutil
import toml

import click
import platform


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def execute(cmd):
    process = subprocess.call(cmd)
    print(process)    

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def init_config(current_dir):
    
    """ For Generating the init configuration file """
    
    print("Genrating a INIT File in",current_dir)
    shutil.copyfile(os.path.join(*[BASE_DIR, 'mlup', 'dsc.toml'])\
        , os.path.join(current_dir,'dsc.toml'))


def main(current_dir):
    
    project_loc = os.path.join(*[BASE_DIR, 'mlup', 'automl'])
    toml_loc = os.path.join(current_dir,'dsc.toml')
    toml_list = toml.load(toml_loc)
    project_name = toml_list['project_name']
    
    print("Making project : ",project_name)
    
    input_dict = []
    
    if os.path.exists(project_name):
        print("File exists")
        exit(0)
    
    os.mkdir(os.path.join(project_loc,project_name))
    copytree(project_loc, project_name+'/')
    
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

    main_string = '        '
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
    shutil.move('views.py', project_name+'/core/')
    print('Done -- Made with Love by DSCVIT')
    return True

   
@click.group(help='A CLI to automatically deploy your ML models')
def cli():
    pass

@cli.command(help='Initialize the configuration file')
def init():
    try:
        init_config(os.getcwd())
        click.echo('Configuration Generated')
    except:
        click.echo('Some error occured')
    

@cli.command(help='Helps you setup your project')
def generate():
    click.echo('Set up Your project')
    main(os.getcwd())

@cli.command(help='Deploy model to heroku')
@click.option('--filename', '-f', required=True, type=str, help='Give the filename of the dir')
def deploy(filename):
    if platform.system() == 'Windows':
        execute(['deploy_heroku.bat', os.path.join(os.getcwd(),filename)])
    else:
        execute(['./deploy_heroku.sh', os.path.join(os.getcwd(),filename)])


if __name__ == "__main__":
    cli()
    


