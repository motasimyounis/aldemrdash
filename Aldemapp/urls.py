from django.urls import path,re_path
from . import views
from django.views.static import serve
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf import settings


urlpatterns = [
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$',serve,{'document_root':settings.STATIC_ROOT}),
    path('', views.home ,name='index'),
    path('exper', views.exper ,name='exper'),
    path('register', views.register_view, name='signup'),
    path('login/', views.custom_login, name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.custom_logout, name='logout'),
    path('student', views.home_student ,name='student'),
    path('profile', views.profile ,name='profile'),
    path('contact', views.contact ,name='contact'),
    path('change_password/',views.change_password, name='change_password'),
    path('playlists/<int:list_id>/', views.playlist ,name='playlist'),
    # path('authorize/', views.google_login, name='google_login'),
    # path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    # path('playlist/', views.fetch_playlist_items, name='fetch_playlist_items'),
    path('watch', views.watch ,name='watch'),
     path('paid', views.paid ,name='paid'),
    path('pakages', views.pakages ,name='pakages'),
    path('get_pdf/<int:document_id>/', views.get_pdf, name='get_pdf'),
    path('view_pdf/<int:document_id>/', views.view_pdf, name='view_pdf'),






    
]
