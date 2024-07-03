from django.contrib import admin
from django.urls import path
from home import views
from .views import upload_image, view_images
from .views import upload_video
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    # path("index", views.index, name='home'),
    path("", views.homee, name='homee'),
    path("index", views.index, name='homee'),
    path("help", views.hellp, name='help'),
    path("about", views.about, name='about'),
    path("services", views.services, name='services'),
    path("contact", views.contact_form, name='contact'),
    path('upload/', upload_image, name='upload_image'),
    path('view/', view_images, name='view_images'),
    path('process/<int:image_id>/', views.process_image, name='process_image'),
    path('upload_video/', upload_video, name='upload_video'),
    # path('login',views.login, name="login"),
    # path('logout',views.logout, name="logout"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('homee/', views.homee, name='homee'),
    path("about2", views.about2, name='about2'),
    path("instructions", views.instructions, name='instructions'),

   
]


