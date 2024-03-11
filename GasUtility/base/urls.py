from django.urls import path , include
from base import views

urlpatterns = [
    path('' , views.login , name='login' ),
   path('register/', views.register, name='register'),
    path('home/' , views.home , name='home' ),
    path('logout/' , views.logout_page , name='logout' ),
    path('send_request/' , views.send_request , name='send_request' ),
]