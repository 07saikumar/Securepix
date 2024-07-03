from django.contrib import admin
from home.models import contact
from .models import UploadedImage
# Register your models here.
admin.site.register(contact)
admin.site.register(UploadedImage)

