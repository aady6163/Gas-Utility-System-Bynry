from django.contrib.auth import authenticate, login as auth_login , logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from base.models import ServiceRequest
from django.contrib import messages

from django.http import HttpResponse, HttpResponseRedirect



def login(request):
    if request.method == "POST":
        username = request.POST.get('login_username')
        password = request.POST.get('login_pass')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Log in the user
            auth_login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Invalid credentials')
    
    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('user_username')
        email = request.POST.get('user_email')
        password = request.POST.get('user_pass')

        try:
            # Attempt to create a new user
            my_user = User.objects.create_user(username=username, email=email, password=password)
            return redirect('login')  # Redirect to the login page after successful registration

        except:
            # Handle the case where the username or email is not unique
            messages.warning(request, "Username Already Exists , try another")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

    return render(request, 'register.html')


@login_required(login_url='login')
def home(request):
    user_service_requests = ServiceRequest.objects.filter(customer=request.user)
    return render(request, 'home.html' , {'service_requests': user_service_requests})

def logout_page(request):
    logout(request)
    messages.success(request, "Logout Succcessful")
    return redirect('login')

@login_required(login_url='login')
def send_request(request):
    if request.method == "POST":
        name = request.POST.get('send_fullName')
        phone = request.POST.get('send_phone')
        address = request.POST.get('send_address')
        request_type = request.POST.get('send_request_type')
        details = request.POST.get('send_details')
        attachment = request.FILES.get('send_attachment')

        try:
            # Create a ServiceRequest object
            service_request = ServiceRequest(
                customer=request.user,  # Assign the current user to the customer field
                name=name,
                address = address,
                contactno = phone ,
                request_type=request_type,
                details=details,
                attachment=attachment,
               
            )
            service_request.save()  # Save the ServiceRequest object
            return redirect('home')  # Success message
        except Exception as e:
            return HttpResponse('Error in form handling: ' + str(e))  
    return render(request, 'send_request.html')
