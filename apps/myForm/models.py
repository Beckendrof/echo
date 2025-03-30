from django.db import models
import uuid

class User(models.Model):
    USER_TYPES = [
        ('creator', 'Creator'),
        ('editor', 'Editor'),
    ]

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255, db_index=True)
    password = models.CharField(max_length=97)
    user_type = models.CharField(max_length=7, choices=USER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

class Creator(models.Model):
    creator_id = models.UUIDField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='creator_profile')
    youtube_channel = models.CharField(max_length=24)
    brand_name = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if self.user:
            self.creator_id = self.user.user_id
        super().save(*args, **kwargs)

class Editor(models.Model):
    editor_id = models.UUIDField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='editor_profile')
    display_name = models.CharField(max_length=50)
    expertise_tags = models.JSONField()

    def save(self, *args, **kwargs):
        if self.user:
            self.editor_id = self.user.user_id
        super().save(*args, **kwargs)
