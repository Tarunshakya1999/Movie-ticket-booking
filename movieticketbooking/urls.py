"""
URL configuration for movieticketbooking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from movieapp.views import *
from django.conf import settings
from django.conf.urls.static import static
from movieapp import views
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',fun1,name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact_view, name='contact'),
    path('policies/', views.policies, name='policies'),
    path('partners/', views.partners, name='partners'),
    path('movie/<int:movie_id>/', views.movie_details, name='movie_detail'),
    path('registration/',views.RegistrationView.as_view(),name='registration'),
    path('login/',login_view,name='login'),
    path('logout/', logout_view, name='logout'),
    path('footer/', footer_view, name='footer'),
    path('profile/',views.ProfileView.as_view(), name="profile"),
    path('updateprofile/<int:pk>',views.UpdateAddress.as_view(),name='updateprofile'),
    path('address/',views.get,name='address'),
    path('error2/', views.error2, name='error2'), 

    
    # Movie ticket
    path('book/', views.book_ticket, name='book_ticket'),
    path("payment-success/<str:ticket_id>/", payment_success, name="payment_success"),
    path("download-ticket/<str:ticket_id>/", download_ticket, name="download_ticket"),
    path('ticket-details/', views.ticket_details, name='ticket_details'),

    path('notfound/', views.ticket_not_found, name='notfound'),
    path('legacy/', views.our_legacy, name='our_legacy'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset/done/', views.password_reset_done, name='password_reset_done'),
   
     
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
