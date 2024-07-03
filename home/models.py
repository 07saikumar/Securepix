from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# makemigrations - create changes and store in a file
# migrate - apply the pending changes created by makemigrations
from django.contrib.auth.models import User
class contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc= models.TextField()
    date = models.DateField()

    def __str__(self):
        return f'Name:{self.name}, {self.email}'  
       
        # return f'Name: {self.name}, Email: {self.email}, Phone: {self.phone}, Date: {self.date}'
        
    

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')  # Field to store the uploaded image
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Field to store the timestamp of when the image was uploaded

    def __str__(self):
        return f'Image uploaded at {self.uploaded_at}'



    