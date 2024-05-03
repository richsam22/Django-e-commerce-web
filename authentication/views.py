from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from .models import User,Contact
from django.http import JsonResponse

# User = settings.AUTH_USER_MODEL


# Create your views here.

def signup(request):
    if request.method == "POST":
       form = UserForm(request.POST)
       if form.is_valid():
           new_user = form.save()
           username = form.cleaned_data.get("username")
           messages.success(request, f"Welcome {username}, your account was created successfully!")
           new_user = authenticate(username=form.cleaned_data["email"], password=form.cleaned_data["password1"])
           
           login(request, new_user)
           return redirect("/", messages)
           
    else: 
        form = UserForm()
        
    context = {
        'form':form
    }
    return render(request, "registration/signup.html", context)

def log_in(request):
    if request.user.is_authenticated:
        messages.warning(request, f"You have already logged in")
        redirect("/")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user =User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
        
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in.")
                return redirect("/")
            else:
                messages.warning(request, "User Does Not Exist, create an account")
                
        except:
                messages.warning(request, f"User with {email} does not exist")
            
        
        
        
    return render(request, "registration/login.html")

def logout(request):
    messages.success(request, f"You logged out")
    return redirect("/login")
    

def contact(request):
    return render(request, "contact.html")

def ajax_contact(request):
    full_name = request.GET["full_name"]
    email = request.GET["email"]
    phone = request.GET["phone"]
    subject = request.GET["subject"]
    message = request.GET["message"]
    
    contact = Contact.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )
    
    data = {
        "bool": True,
        "message": "Message Sent Successfully"
    }
    
    return JsonResponse({"data": data})

