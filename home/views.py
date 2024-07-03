from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from home.models import contact
from django.contrib import messages
from .models import UploadedImage
import cv2
import base64
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .forms import CustomUserCreationForm
import os
from PIL import Image
import io
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from django.conf import settings
import mimetypes

# from .forms import UploadImageForm 
# Create your views here.
def homee(request):
    return render(request, 'homee.html')
def hellp(request):
    return render(request, 'help.html')


#authentication

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page or home page after successful registration
        else:
            return render(request, 'register.html', {'form': form, 'error': form.errors})
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        # Get the username and password from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        # If the user is authenticated, log them in and redirect to homee.html
        if user is not None:
            auth_login(request, user)
            # return redirect('index.html')
            return render(request, 'index.html')
        
        else:
            # If authentication fails, return an error message
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

def index(request):
    
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def about2(request):
    return render(request, 'about2.html')
def instructions(request):
    return render(request, 'instructions.html')

def services(request):
    return render(request, 'services.html')
#login
def login(request):
    render(request,'login.html')

def logout(request):
    render(request,'index.html')



#contact form

def contact_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        new_contact = contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        new_contact.save()
        messages.success(request, "Your message has been sent!")
    return render(request, 'contact.html')


# upload images
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            # Validate the file type
            valid_image_mime_types = ['image/jpeg', 'image/png', 'image/gif']
            if image.content_type not in valid_image_mime_types:
                messages.error(request, "Invalid file type. Please upload an image (JPEG, PNG, GIF).")
                return render(request, 'upload_image.html')
            
            # Create a new UploadedImage object and save it to the database
            uploaded_image = UploadedImage(image=image)
            uploaded_image.save()
            
            # Redirect to the view images page after successful upload
            return redirect('view_images')
        else:
            messages.error(request, "No image provided.")
    
    # Render the upload image form template for GET requests
    return render(request, 'upload_image.html')


#view images
def view_images(request):
    images = UploadedImage.objects.all()
    image_data = []

    for image in images:
        image_path = image.image.path
        image_size = os.path.getsize(image_path)
        image_data.append({
            'image': image,
            'size': image_size,
        })

    return render(request, 'view_images.html', {'images': image_data})




# Function to handle image processing requests

def process_image(request, image_id):
    try:
        # Retrieve the uploaded image
        uploaded_image = UploadedImage.objects.get(pk=image_id)

        # Read the image using OpenCV
        image = cv2.imread(uploaded_image.image.path)

        # Load the cascade classifier for face detection
        cascades_path = 'cascades/'  # Update this path to the directory containing the cascade classifier XML files
        face_cascade = cv2.CascadeClassifier(cascades_path + 'haarcascade_frontalface_default.xml')

        # Verify if the cascade classifier loaded successfully
        if face_cascade.empty():
            return HttpResponse("Error loading cascade classifier.")

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=12, minSize=(30, 30))

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi = image[y:y + h, x:x + w]
            blur = cv2.GaussianBlur(roi, (45, 45), 20)
            image[y:y + h, x:x + w] = blur

        # Perform image flipping using OpenCV
        flipped_image = cv2.flip(image, 1)  # Flip horizontally

        # Convert the processed image to JPEG format
        _, processed_image_data = cv2.imencode('.jpg', flipped_image)

        # Encode the processed image data as base64
        processed_image_base64 = base64.b64encode(processed_image_data).decode('utf-8')

        # Calculate the size of the processed image in bytes
        image_size = len(processed_image_data)

        # Pass the processed image data to the template for rendering
        return render(request, 'processed_image.html', {
            'processed_image': processed_image_base64,
            'image_size': image_size
        })
    except Exception as e:
        # Handle exceptions, such as image not found or processing errors
        return HttpResponse("Error processing image: " + str(e))


# # #video processing


def upload_video(request):
    error_message = None
    if request.method == 'POST' and request.FILES.get('video'):
        video = request.FILES['video']
        if not video.content_type.startswith('video'):
            error_message = "Invalid file type. Please upload a video file."
        else:
            fs = FileSystemStorage()
            # Save the uploaded video to a temporary location
            uploaded_video_path = fs.save(video.name, video)
            uploaded_video_full_path = fs.path(uploaded_video_path)

            # Process the video and save the processed video
            processed_video_path = process_video(uploaded_video_full_path)

            # Delete the uploaded video from the server
            os.remove(uploaded_video_full_path)

            # Automatically download the processed video
            response = FileResponse(open(processed_video_path, 'rb'), as_attachment=True)

           
            response['X-Sendfile'] = processed_video_path

            return response

    return render(request, 'upload_video.html', {'error_message': error_message})

def process_video(video_path):
    # Load the cascade classifier
    cascades_path = 'cascades/'  # Update this to the correct path where your XML file is located
    face_cascade = cv2.CascadeClassifier(cascades_path + 'haarcascade_frontalface_default.xml')

    if face_cascade.empty():
        raise Exception("Error loading cascade classifier")

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Error opening video file")

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create a VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    processed_video_path = 'processed_video.mp4'
    out = cv2.VideoWriter(processed_video_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        frame_with_blurred_faces = blur_faces(frame, faces)
        out.write(frame_with_blurred_faces)

    cap.release()
    out.release()

    return processed_video_path




    

def blur_faces(img, faces):
    for (x, y, w, h) in faces:
        roi = img[y:y+h, x:x+w]
        blurred_roi = cv2.GaussianBlur(roi, (45, 45), 20)
        img[y:y+h, x:x+w] = blurred_roi
    return img
