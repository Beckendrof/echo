from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        messages.success(request, "Registration successful!")
        # return redirect('login')  # Redirect to login page after registration
    
    return render(request, 'register.html')

def apply_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        job_titles = request.POST.getlist('job_title[]')
        company_names = request.POST.getlist('company_name[]')
        years_worked = request.POST.getlist('years[]')
        
        if 'resume' in request.FILES:
            resume = request.FILES['resume']
            # Save the resume file
        
        messages.success(request, "Application submitted successfully!")
        # return redirect('application_success')  # Redirect to a success page
    
    return render(request, 'apply.html')

def home_view(request):
    return render(request, 'home.html')
