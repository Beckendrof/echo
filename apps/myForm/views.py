from django.shortcuts import render, redirect
from django.contrib import messages
from utils.storage.factory import get_job_application_repository, get_user_registration_repository

def register_view(request):
    if request.method == 'POST':
        repo = get_user_registration_repository()
        
        try:
            user_data = {
                'first_name': request.POST.get('first_name', ''),
                'last_name': request.POST.get('last_name', ''),
                'email': request.POST.get('email', ''),
                'username': request.POST.get('username', ''),
                'password': request.POST.get('password', '')
            }
            
            repo.create(user_data)
            messages.success(request, "Registration successful!")
            
            return redirect('home')
        except Exception as e:
            return redirect('register')
    else:
        return redirect('register')



def apply_view(request):
    if request.method == 'POST':
        # Get repository
        repo = get_job_application_repository()
        
        # Create application
        application_data = {
            'first_name': request.POST.get('first_name', ''),
            'last_name': request.POST.get('last_name', ''),
            'email': request.POST.get('email', ''),
            'phone': request.POST.get('phone', '')
        }

        if 'resume' in request.FILES:
            application_data['resume'] = request.FILES['resume']
        
        # Save application
        application = repo.create(application_data)
        
        # Save job experiences
        job_titles = request.POST.getlist('job_title[]')
        company_names = request.POST.getlist('company_name[]')
        years_worked = request.POST.getlist('years[]')
        
        try:
            for i in range(len(job_titles)):
                if i < len(company_names) and i < len(years_worked):
                    experience_data = {
                        'job_title': job_titles[i],
                        'company_name': company_names[i],
                        'years': int(years_worked[i])
                    }
                    repo.create_related(application['id'], experience_data)
            
            messages.success(request, "Application submitted successfully!")
            return redirect('home')
        except Exception as e:
            return redirect('apply')
    else:
        return redirect('apply')


def apply(request):
    return render(request, 'apply.html')

def register(request):
    return render(request, 'register.html')

def home_view(request):
    return render(request, 'home.html')
