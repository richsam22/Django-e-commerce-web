from django.urls import path
from .views import *



app_name = "authentication"

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', log_in, name='login'),
    path('logout/', logout, name='logout'),
    
    
    ######### contact  #####
    path('contact/', contact, name='contact'),
    
    ######### contact  #####
    path('ajax-contact-form/', ajax_contact, name='ajax-contact-form'),
]


