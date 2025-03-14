# utils/storage/base.py
from abc import ABC, abstractmethod

class Repository(ABC):
    """Base repository interface"""
    
    @abstractmethod
    def create(self, data):
        pass
    
    @abstractmethod
    def get(self, id):
        pass
    
    @abstractmethod
    def get_all(self):
        pass
    
    @abstractmethod
    def update(self, id, data):
        pass
    
    @abstractmethod
    def delete(self, id):
        pass

class RelationalRepository(Repository):
    """Interface for storing relational data"""
    
    @abstractmethod
    def create_related(self, parent_id, data):
        """Create a related entity"""
        pass
    
    @abstractmethod
    def get_related(self, parent_id):
        """Get related entities"""
        pass

class NonRelationalRepository(Repository):
    """Interface for storing non-relational data"""
    
    @abstractmethod
    def find_by_field(self, field, value):
        """Find documents by field value"""
        pass
