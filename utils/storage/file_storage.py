# utils/storage/file_storage.py
import os
import json
import uuid
from datetime import datetime

from utils.storage.base import RelationalRepository, NonRelationalRepository

class FileStorageRepository:
    """Base file storage functionality"""
    
    def __init__(self, storage_dir):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
    
    def _generate_id(self):
        return str(uuid.uuid4())
    
    def _get_file_path(self, id):
        return os.path.join(self.storage_dir, f"{id}.json")
    
    def _save_file(self, file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _load_file(self, file_path):
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def _list_files(self):
        if not os.path.exists(self.storage_dir):
            return []
        return [f for f in os.listdir(self.storage_dir) if f.endswith('.json')]

class JobApplicationFileStorage(RelationalRepository, FileStorageRepository):
    """Store job applications in files"""
    
    def __init__(self):
        base_dir = os.path.join('data', 'relational', 'job_applications')
        FileStorageRepository.__init__(self, base_dir)
        self.uploads_dir = os.path.join('data', 'uploads', 'resumes')
        os.makedirs(self.uploads_dir, exist_ok=True)
    
    def create(self, data):
        """Create a new job application"""
        id = self._generate_id()
        
        # Handle file upload if present
        resume_path = None
        if 'resume' in data:
            resume = data['resume']
            if hasattr(resume, 'name'):  # It's a file object
                filename = f"{id}_{resume.name}"
                resume_path = os.path.join(self.uploads_dir, filename)
                
                # Save the file
                with open(resume_path, 'wb+') as destination:
                    for chunk in resume.chunks():
                        destination.write(chunk)
                
                # Store just the relative path
                resume_path = os.path.join('resumes', filename)
        
        # Create application record
        record = {
            'id': id,
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
            'email': data.get('email', ''),
            'phone': data.get('phone', ''),
            'resume': resume_path,
            'created_at': datetime.now().isoformat()
        }
        
        file_path = self._get_file_path(id)
        self._save_file(file_path, record)
        
        return record
    
    def get(self, id):
        """Get job application by ID"""
        file_path = self._get_file_path(id)
        return self._load_file(file_path)
    
    def get_all(self):
        """Get all job applications"""
        result = []
        for filename in self._list_files():
            id = filename.replace('.json', '')
            data = self.get(id)
            if data:
                result.append(data)
        return result
    
    def update(self, id, data):
        """Update a job application"""
        file_path = self._get_file_path(id)
        existing_data = self._load_file(file_path)
        
        if not existing_data:
            return None
        
        # Update fields
        for key, value in data.items():
            if key != 'id' and key != 'created_at':
                existing_data[key] = value
        
        self._save_file(file_path, existing_data)
        return existing_data
    
    def delete(self, id):
        """Delete a job application"""
        file_path = self._get_file_path(id)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    
    def create_related(self, parent_id, data):
        """Create job experience related to an application"""
        # Initialize experience storage if needed
        exp_storage = JobExperienceFileStorage()
        data['application_id'] = parent_id
        return exp_storage.create(data)
    
    def get_related(self, parent_id):
        """Get experiences for an application"""
        exp_storage = JobExperienceFileStorage()
        return exp_storage.get_by_application(parent_id)

class JobExperienceFileStorage(FileStorageRepository):
    """Store job experiences in files"""
    
    def __init__(self):
        base_dir = os.path.join('data', 'relational', 'job_experiences')
        super().__init__(base_dir)

    def create(self, data):
        """Create a new job experience"""
        id = self._generate_id()
        record = {
            'id': id,
            'application_id': data.get('application_id'),
            'job_title': data.get('job_title', ''),
            'company_name': data.get('company_name', ''),
            'years': data.get('years', 0)
        }
        
        file_path = self._get_file_path(id)
        self._save_file(file_path, record)
        
        return record
    
    def get(self, id):
        """Get job experience by ID"""
        file_path = self._get_file_path(id)
        return self._load_file(file_path)
    
    def get_all(self):
        """Get all job experiences"""
        result = []
        for filename in self._list_files():
            id = filename.replace('.json', '')
            data = self.get(id)
            if data:
                result.append(data)
        return result
    
    def get_by_application(self, application_id):
        """Get all experiences for a specific application"""
        result = []
        for filename in self._list_files():
            id = filename.replace('.json', '')
            data = self.get(id)
            if data and data.get('application_id') == application_id:
                result.append(data)
        return result
    
    def update(self, id, data):
        """Update a job experience"""
        file_path = self._get_file_path(id)
        existing_data = self._load_file(file_path)
        
        if not existing_data:
            return None
        
        # Update fields
        for key, value in data.items():
            if key != 'id' and key != 'application_id':
                existing_data[key] = value
        
        self._save_file(file_path, existing_data)
        return existing_data
    
    def delete(self, id):
        """Delete a job experience"""
        file_path = self._get_file_path(id)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

class UserRegistrationFileStorage(NonRelationalRepository, FileStorageRepository):
    """Store user registrations in files"""
    
    def __init__(self):
        base_dir = os.path.join('data', 'nonrelational', 'registrations')
        super().__init__(base_dir)
    
    def create(self, data):
        """Create a new user registration"""
        id = self._generate_id()
        
        # Check if username/email already exists
        if self.find_by_field('username', data.get('username')):
            raise ValueError("Username already exists")
        
        if self.find_by_field('email', data.get('email')):
            raise ValueError("Email already exists")
        
        # Create registration record
        record = {
            'id': id,
            'username': data.get('username', ''),
            'email': data.get('email', ''),
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
            'password': data.get('password', ''),  # In a real app, this should be hashed
            'created_at': datetime.now().isoformat()
        }
        
        file_path = self._get_file_path(id)
        self._save_file(file_path, record)
        
        return record
    
    def get(self, id):
        """Get user registration by ID"""
        file_path = self._get_file_path(id)
        return self._load_file(file_path)
    
    def get_all(self):
        """Get all user registrations"""
        result = []
        for filename in self._list_files():
            id = filename.replace('.json', '')
            data = self.get(id)
            if data:
                result.append(data)
        return result
    
    def find_by_field(self, field, value):
        """Find users by a field value"""
        result = []
        for filename in self._list_files():
            id = filename.replace('.json', '')
            data = self.get(id)
            if data and data.get(field) == value:
                result.append(data)
        return result
    
    def update(self, id, data):
        """Update a user registration"""
        file_path = self._get_file_path(id)
        existing_data = self._load_file(file_path)
        
        if not existing_data:
            return None
        
        # Update fields
        for key, value in data.items():
            if key != 'id' and key != 'created_at':
                existing_data[key] = value
        
        self._save_file(file_path, existing_data)
        return existing_data
    
    def delete(self, id):
        """Delete a user registration"""
        file_path = self._get_file_path(id)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
