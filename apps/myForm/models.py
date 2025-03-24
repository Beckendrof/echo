from django.db import models

class JobApplication(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Application by {self.first_name} {self.last_name}"

class JobExperience(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='experiences')
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    years = models.IntegerField()
    
    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

class UserRegistration(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

import uuid

class User(models.Model):
    USER_TYPES = [
        ('creator', 'Creator'),
        ('editor', 'Editor'),
    ]

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255, db_index=True)
    password_hash = models.CharField(max_length=97)  # Bcrypt hash (salt + hash)
    user_type = models.CharField(max_length=7, choices=USER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Creator(models.Model):
    creator_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='creator_profile')
    youtube_channel = models.CharField(max_length=24)
    brand_name = models.CharField(max_length=50)

    def __str__(self):
        return self.brand_name

class Editor(models.Model):
    editor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='editor_profile')
    display_name = models.CharField(max_length=50)
    expertise_tags = models.JSONField()

    def __str__(self):
        return self.display_name
