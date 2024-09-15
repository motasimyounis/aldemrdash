from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.contrib.auth import update_session_auth_hash
import uuid
from django.http import JsonResponse
from django.utils import timezone
import google.auth.transport.requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import os
import json
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.http import StreamingHttpResponse, HttpResponse, Http404
from wsgiref.util import FileWrapper
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2 import PdfReader, PdfWriter
import platform
import io
from django.http import HttpResponseForbidden
from django.http import FileResponse
import socket
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
import httpagentparser
from django.db import transaction
import uuid
from django.http import HttpResponse
import psutil
import random ,re
import string

from django.core.mail import send_mail

from django_user_agents.utils import get_user_agent




def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


def get_mac_address():
    mac_address = None
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                mac_address = addr.address
                break
        if mac_address:
            break
    return mac_address





def home(request):    
    video = Videos.objects.all()
    context = {
        'video' : video
    }
    return render(request,'index.html',context)


def exper(request):
    expr =  Services.objects.all()
    searched = ''
    if request.method == 'POST':
        searched = request.POST['searched']
        expr = Services.objects.filter(name__contains=searched)
        if expr:
            messages.add_message(request, messages.SUCCESS, ' طلبك موجود ✔️✔️')
        else:
            messages.add_message(request, messages.SUCCESS, ' طلبك غير موجود ❌❌')
            return redirect('exper')
    
    context = {
        'expr':expr,
        'searched':searched,

    }
    return render(request,'exper.html',context)







@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.add_message(request, messages.SUCCESS, ' تم تغيير كلمة السر بنجاح')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'students/change_password.html', {'form': form})







def set_device_token(response, user):
    token = str(uuid.uuid4())
    user.device_token = token
    user.save()
    response.set_cookie('device_token', token, httponly=True, secure=True)


def remove_browser_info(user_agent):
    # Regular expression to match and remove browser version (like Edg/128.0.0.0)
    # This regex matches patterns like Edg/x.x.x.x, Chrome/x.x.x.x, etc.
    cleaned_user_agent = re.sub(r'(Edg/\d+\.\d+\.\d+\.\d+|Chrome/\d+\.\d+\.\d+\.\d+)', '', user_agent)
    return cleaned_user_agent.strip()



@transaction.atomic
def register_view(request):
    if request.method == 'POST':
        device_id = request.POST['device_id']
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            device_id = str(uuid.uuid4())  # Generate a unique device ID
            user.device_id = device_id
            print(user.device_id)
            user.save()
            user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
            cleaned_user_agent = remove_browser_info(user_agent)
            user.user_agent = cleaned_user_agent    
            print(user.user_agent)
            response = JsonResponse({'message': 'User registered successfully!'})
            response.set_cookie('device_id', device_id)  # Set the device ID in a cookie
            print(request.COOKIES.get('device_id'))
            confirmation_code = generate_code()
            print(confirmation_code)
            subject = 'كود خصم الأستاذة الدمرداش'
            message =  f"""انسخ كود الخاص بك وأرسله الى الأستاذة لإكمال اجراءات الدفع :{confirmation_code}
            https://chatgpt.com/
            """
            recipient_list  =[ form.cleaned_data['email']]

            send_mail(subject, message, 'mtsmy31@gmail.com', recipient_list)
            return redirect('paid')  # Redirect to a home page after registration
    
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def custom_logout(request):
    if request.method == 'GET':
        logout(request)
        messages.success(request, 'تم تسجيل خروجك ')
        return HttpResponseRedirect(reverse('login'))  
    

    


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            device_id  = form.cleaned_data.get('device_id ')
            user = authenticate(username=username, password=password)
            if user is not None:
                is_paidd = True
                if user.is_paid ==  is_paidd:
                    login(request, user)
                    return redirect('student')
                    # device_id_cookie = request.COOKIES.get('device_id')
                    # print(device_id_cookie)
                    # if user.device_id == device_id_cookie:
                    #     login(request, user)
                    #     return redirect('student')
                    # else:
                    #     messages.error(request, "Login not allowed from this device.")
                
                else:
                    messages.error(request, f' يجب عليك الدفع أولاً')
                    return redirect('paid')
            else:
                messages.error(request, 'اسم المستخدم أو كلمة السر خطأ')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة السر خطأ')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})





@login_required
def home_student(request):
    user = request.user
    user = User.objects.get(username=user.username)
    subjects = user.subjects.all()

    # for subject in subjects:
    #     print(subject.id)
    #     print(subject.name)
    #     print(subject.url)



    print("System:", platform.system())
    print("Node Name:", platform.node())
    print("Release:", platform.release())
    print("Version:", platform.version())
    print("Machine:", platform.machine())
    print("Processor:", platform.processor())

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    print("Hostname:", hostname)
    print("IP Address:", ip_address)



    net_info = psutil.net_if_addrs()

    for interface, addrs in net_info.items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:  # AF_LINK indicates MAC address
                print(f"Interface: {interface}, MAC Address: {addr.address}")


    sub = Subject.objects.all()
    context = {
        'sub' : sub,
        'user': user,
        'subjects': subjects
    }
    return render(request,'students/home.html',context)



@login_required
def profile(request):
    # totalitem = 0
    user = request.user
    # data_items = Data.objects.filter(pdf=0)
    # totalitem = len(data_items)
    # print(totalitem)
    sub_name = Subject.objects.all()
    return render(request,'students/profile.html',{sub_name:'sub_name'})




def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'تم إرسال رسالتك وسيتم التواصل معك بأقرب وقت')
            return redirect('contact')  # Redirect to a home page after registration
    else:
        form = ContactForm()
    context = {
        'form' : form
    }
    return render(request,'students/contact.html',context)




@login_required
def playlist(request,list_id):
    lists = get_object_or_404(Subject, id=list_id)
    context = {
        'lists' : lists
    }
   
    return render(request,'students/playlist.html',context)


# CLIENT_SECRETS_FILE = 'E:/Files/Al-DEMERDASH/Aldempro/client_secret.json'
# SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
# API_SERVICE_NAME = 'youtube'
# API_VERSION = 'v3'


# def get_authenticated_service(credentials):
#     return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

# def authorize(request):
#     flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#         CLIENT_SECRETS_FILE, scopes=SCOPES)
#     flow.redirect_uri = request.build_absolute_uri('/oauth2callback/')

#     authorization_url, state = flow.authorization_url(
#         access_type='offline',
#         include_granted_scopes='true')

#     request.session['state'] = state
#     return redirect(authorization_url)



# def oauth2callback(request):
#     state = request.session['state']
#     flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#         CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
#     flow.redirect_uri = request.build_absolute_uri('/oauth2callback')

#     authorization_response = request.build_absolute_uri()
#     flow.fetch_token(authorization_response=authorization_response)

#     credentials = flow.credentials
#     request.session['credentials'] = credentials_to_dict(credentials)
    
#     return redirect('fetch_playlist_items')

# def credentials_to_dict(credentials):
#     return {'token': credentials.token,
#             'refresh_token': credentials.refresh_token,
#             'token_uri': credentials.token_uri,
#             'client_id': credentials.client_id,
#             'client_secret': credentials.client_secret,
#             'scopes': credentials.scopes}

# @login_required
# def fetch_playlist_items(request):
#     if 'credentials' not in request.session:
#         return redirect('authorize')

#     credentials = google.oauth2.credentials.Credentials(
#         **request.session['credentials'])

#     youtube = get_authenticated_service(credentials)
    
#     # Get the logged-in user's email
#     user_email = request.user.email

#     # Check if user email has access to the playlist
#     authorized_emails = ['mtsmy31@gmail.com']  # Add your authorized emails here
#     if user_email not in authorized_emails:
#         return render(request, 'unauthorized.html')

#     playlist_id = 'PLXcMwxvA7BStUYjAEJLFtb0D_X7aAU1hw&si=sm-F_JCOhnDNX-Pe'  # Replace with your playlist ID
#     request = youtube.playlistItems().list(
#         part='snippet',
#         maxResults=25,
#         playlistId=playlist_id
#     )
#     response = request.execute()
    
#     playlist_items = response.get('items', [])
    
#     context = {
#         'playlist_items': playlist_items
#     }
    
    
#     return render(request, 'students/playlist.html', context)



# def google_login(request):
#     flow = Flow.from_client_secrets_file(
#         'client_secret.json',
#         scopes=['https://www.googleapis.com/auth/youtube.readonly'],
#         redirect_uri='http://localhost:8000/oauth2callback/')
#     authorization_url, state = flow.authorization_url(
#         access_type='offline',
#         include_granted_scopes='true')

#     request.session['state'] = state
#     return redirect(authorization_url)

# def oauth2callback(request):
#     state = request.session['state']
#     flow = Flow.from_client_secrets_file(
#         'client_secret.json',
#         scopes=['https://www.googleapis.com/auth/youtube.readonly'],
#         state=state,
#         redirect_uri='http://localhost:8000/oauth2callback/')
#     flow.fetch_token(authorization_response=request.build_absolute_uri())

#     credentials = flow.credentials
#     request.session['credentials'] = credentials_to_dict(credentials)
#     return redirect('profile')

# def fetch_playlist_items(request):
#     if 'credentials' not in request.session:
#         return redirect('google_login')

#     credentials = Credentials(**request.session['credentials'])
#     youtube = build('youtube', 'v3', credentials=credentials)

#     playlists = youtube.playlists().list(
#         part='snippet,contentDetails',
#         mine=True
#     ).execute()

#     return render(request, 'students/playlist.html', {'playlists': playlists})

# def credentials_to_dict(credentials):
#     return {
#         'token': credentials.token,
#         'refresh_token': credentials.refresh_token,
#         'token_uri': credentials.token_uri,
#         'client_id': credentials.client_id,
#         'client_secret': credentials.client_secret,
#         'scopes': credentials.scopes
#     }


def paid(request):
    return render(request,'paid.html')


def watch(request):
    return render(request,'students/watch-video.html')



# def preprocess_points(points):
#     return points.split('\n')

# In your view function or class-based view context

def pakages(request):
    package = Package.objects.all()

    # pointslist = Package.objects.all()
    # points_list = pointslist.points.split('\n')
    context = {
        'package':package,
       
    }    
    return render(request,'pakages.html',context)




def get_pdf(request, document_id):
    document = get_object_or_404(Subject, id=document_id)
    if not request.user.has_perm('view_document', document):
        return HttpResponseForbidden("You don't have permission to view this file.")
    
    with open(document.pdf.path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(document.subject)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-Download-Options'] = 'noopen'
        return response

def view_pdf(request, document_id):
    document = get_object_or_404(Subject, id=document_id)
    if not request.user.has_perm('view_document', document):
        return HttpResponseForbidden("You don't have permission to view this file.")
    return render(request, 'students/view_pdf.html', {'document': document})


