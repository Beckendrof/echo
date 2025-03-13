from utils.storage.base import RelationalRepository, NonRelationalRepository
from apps.myForm.models import JobApplication, JobExperience, UserRegistration

class JobApplicationDbStorage(RelationalRepository):
    """Store job applications in a relational database"""
    
    def create(self, data):
        """When you're ready to use a database, implement this method"""
        application = JobApplication(
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', '')
        )
        
        if 'resume' in data:
            application.resume = data['resume']
            
        application.save()
        return application
    
    def get(self, id):
        try:
            return JobApplication.objects.get(pk=id)
        except JobApplication.DoesNotExist:
            return None
    
    def get_all(self):
        return JobApplication.objects.all()
    
    def update(self, id, data):
        try:
            application = JobApplication.objects.get(pk=id)
            for key, value in data.items():
                if hasattr(application, key):
                    setattr(application, key, value)
            application.save()
            return application
        except JobApplication.DoesNotExist:
            return None
    
    def delete(self, id):
        try:
            application = JobApplication.objects.get(pk=id)
            application.delete()
            return True
        except JobApplication.DoesNotExist:
            return False
    
    def create_related(self, parent_id, data):
        try:
            application = JobApplication.objects.get(pk=parent_id)
            experience = JobExperience(
                application=application,
                job_title=data.get('job_title', ''),
                company_name=data.get('company_name', ''),
                years=data.get('years', 0)
            )
            experience.save()
            return experience
        except JobApplication.DoesNotExist:
            return None
    
    def get_related(self, parent_id):
        try:
            application = JobApplication.objects.get(pk=parent_id)
            return application.experiences.all()
        except JobApplication.DoesNotExist:
            return []

class UserRegistrationDbStorage(NonRelationalRepository):
    """Store user registrations in a non-relational database"""
    
    def create(self, data):
        """When you're ready to use a database, implement this method"""
        user = UserRegistration(
            username=data.get('username', ''),
            email=data.get('email', ''),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            password=data.get('password', '')  # Should be hashed in real implementation
        )
        user.save()
        return user
    
    def get(self, id):
        try:
            return UserRegistration.objects.get(pk=id)
        except UserRegistration.DoesNotExist:
            return None
    
    def get_all(self):
        return UserRegistration.objects.all()
    
    def find_by_field(self, field, value):
        query = {field: value}
        return UserRegistration.objects.filter(**query)
    
    def update(self, id, data):
        try:
            user = UserRegistration.objects.get(pk=id)
            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            user.save()
            return user
        except UserRegistration.DoesNotExist:
            return None
    
    def delete(self, id):
        try:
            user = UserRegistration.objects.get(pk=id)
            user.delete()
            return True
        except UserRegistration.DoesNotExist:
            return False
