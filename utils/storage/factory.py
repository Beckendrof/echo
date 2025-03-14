# utils/storage/factory.py
import os

# Import storage implementations
from utils.storage.file_storage import (
    JobApplicationFileStorage,
    UserRegistrationFileStorage
)

# For future use
from utils.storage.db_storage import (
    JobApplicationDbStorage,
    UserRegistrationDbStorage
)

# Current mode - change to 'db' when ready to use database
STORAGE_MODE = 'file'

def get_job_application_repository():
    """Get the appropriate job application repository"""
    if STORAGE_MODE == 'file':
        return JobApplicationFileStorage()
    else:
        return JobApplicationDbStorage()

def get_user_registration_repository():
    """Get the appropriate user registration repository"""
    if STORAGE_MODE == 'file':
        return UserRegistrationFileStorage()
    else:
        return UserRegistrationDbStorage()
