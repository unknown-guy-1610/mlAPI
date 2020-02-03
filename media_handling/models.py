from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class app_name(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    app = models.CharField(max_length=200,unique=True)
    classifier_file = models.FileField(upload_to='ClassifierFile')
    model_file = models.FileField(upload_to='modelFiles')
    toml_file = models.FileField(upload_to='TOML_Files')
    url = models.URLField(unique=True,blank=True)
