from django.shortcuts import render, redirect
from django.contrib import messages
import logging
from .forms import CombinedRegistrationForm
from django.contrib.auth import authenticate, login
from utils.storage.factory import get_job_application_repository, get_user_registration_repository
logger = logging.getLogger('django')

def signup(request):
    if request.method == 'POST':
        form = CombinedRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
        else:
            pass

    else:
        form = CombinedRegistrationForm()
        # repo = get_user_registration_repository()

        # email = request.POST.get('email')
        # password = request.POST.get('password')
        # user_type = request.POST.get('user_type')
        
        # user_data = {
        #     'email': email,
        #     'password': password,
        #     'user_type': user_type
        # }
        
        # if user_type == 'creator':
        #     user_data['youtube_channel'] = request.POST.get('youtube_channel')
        #     user_data['brand_name'] = request.POST.get('brand_name')
        # elif user_type == 'editor':
        #     user_data['display_name'] = request.POST.get('display_name')
        #     user_data['expertise_tags'] = request.POST.get('expertise_tags')
        
        # try:
        #     repo.create(user_data)
        #     logger.success(request, 'Account created successfully')
        #     return redirect('home')
        # except Exception as e:
        #     logger.error(request, f'Error creating account: {str(e)}')
        #     return redirect('home')
    
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me') == 'on'
        
        try:
            user = repo_login(email, password)
            
            if user is not None:
                login(request, user)
                
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                
                messages.success(request, 'Login successful')
                return redirect('home')  # Redirect to dashboard or appropriate page
            else:
                messages.error(request, 'Invalid email or password')
        except Exception as e:
            messages.error(request, f'Error during login: {str(e)}')
        
        return redirect('login')
    
    return render(request, 'login.html')

def repo_login(email, password):
    # This function should implement the actual login logic
    # It should verify the email and password against your database or authentication system
    # Return a user object if login is successful, None otherwise
    # Example:
    user = authenticate(email=email, password=password)
    return user
    
    return render(request, "login.html")

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

def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')