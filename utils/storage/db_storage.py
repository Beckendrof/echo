from utils.storage.base import RelationalRepository, NonRelationalRepository
from apps.myForm.models import JobApplication, JobExperience, User, Creator, Editor
from django.contrib.auth.hashers import make_password

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

class UserDbStorage(NonRelationalRepository):
    """Store users and their profiles in the database"""
    
    def create(self, data):
        """Create a user with appropriate profile based on user_type"""
        try:
            # Create base user
            user = User.objects.create(
                email=data['email'],
                password_hash=make_password(data['password']),
                user_type=data['user_type'],
                is_verified=False
            )
            
            # Create profile based on user type
            if data['user_type'] == 'creator':
                Creator.objects.create(
                    user=user,
                    youtube_channel=data.get('youtube_channel', ''),
                    brand_name=data.get('brand_name', '')
                )
            elif data['user_type'] == 'editor':
                Editor.objects.create(
                    user=user,
                    display_name=data.get('display_name', ''),
                    expertise_tags=data.get('expertise_tags', [])
                )
            
            return user
        except Exception as e:
            # Handle unique constraint violations etc.
            raise ValueError(f"User creation failed: {str(e)}")

    def get(self, user_id):
        try:
            return User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return None

    def get_all(self):
        return User.objects.all()

    def find_by_field(self, field, value):
        """Find users by any field, including related profile fields"""
        try:
            # Handle profile-related searches
            if field in ['youtube_channel', 'brand_name']:
                return User.objects.filter(creator_profile__**{field: value})
            if field in ['display_name', 'expertise_tags']:
                return User.objects.filter(editor_profile__**{field: value})
            
            return User.objects.filter(**{field: value})
        except Exception as e:
            raise ValueError(f"Invalid search field: {str(e)}")

    def update(self, user_id, data):
        try:
            user = User.objects.get(user_id=user_id)
            
            # Update base user fields
            for field in ['email', 'user_type', 'is_verified']:
                if field in data:
                    setattr(user, field, data[field])
            
            # Update password if provided
            if 'password' in data:
                user.password_hash = make_password(data['password'])
            
            user.save()
            
            # Update profile data if present
            if user.user_type == 'creator' and user.creator_profile:
                for field in ['youtube_channel', 'brand_name']:
                    if field in data:
                        setattr(user.creator_profile, field, data[field])
                user.creator_profile.save()
            
            if user.user_type == 'editor' and user.editor_profile:
                for field in ['display_name', 'expertise_tags']:
                    if field in data:
                        setattr(user.editor_profile, field, data[field])
                user.editor_profile.save()
            
            return user
        except User.DoesNotExist:
            return None

    def delete(self, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False
