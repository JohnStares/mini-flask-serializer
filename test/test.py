import unittest
import json
from typing import Dict, Any

# I installed the package in development mode to test it out here
from mini_flask_serializer import MiniFlaskSerializer


class TestMiniFlaskSerializer(unittest.TestCase):
    def setUp(self):
        self.serializer = MiniFlaskSerializer()
    
    # Test class with to_dict method
    class TestModelWithToDict:
        def __init__(self, id: int, name: str, email: str, password: str):
            self.id = id
            self.name = name
            self.email = email
            self.password = password
        
        def to_dict(self) -> Dict[str, Any]:
            return {
                'id': self.id,
                'name': self.name,
                'email': self.email,
                'password': self.password
            }
    
    # Test class with to_json method
    class TestModelWithToJson:
        def __init__(self, id: int, username: str, is_active: bool):
            self.id = id
            self.username = username
            self.is_active = is_active
        
        def to_json(self) -> str:
            return json.dumps({
                'id': self.id,
                'username': self.username,
                'is_active': self.is_active
            })
    
    # Test class without serialization methods
    class TestRegularModel:
        def __init__(self, id: int, title: str, content: str, secret: str):
            self.id = id
            self.title = title
            self.content = content
            self.secret = secret
            self._private_attr = "should_be_ignored"
    
    def test_to_dict_method(self):
        """Test serialization with to_dict method"""
        obj = self.TestModelWithToDict(1, "John Doe", "john@example.com", "secret123")
        result = self.serializer.serializer(obj)
        
        expected = {
            'id': 1,
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'secret123'
        }
        self.assertEqual(result, expected)
    
    def test_to_json_method(self):
        """Test serialization with to_json method"""
        obj = self.TestModelWithToJson(2, "johndoe", True)
        result = self.serializer.serializer(obj)
        
        expected = {
            'id': 2,
            'username': 'johndoe',
            'is_active': True
        }
        self.assertEqual(result, expected)
    
    def test_regular_object(self):
        """Test serialization with regular object without serialization methods"""
        obj = self.TestRegularModel(3, "Test Title", "Test Content", "secret")
        result = self.serializer.serializer(obj)
        
        expected = {
            'id': 3,
            'title': 'Test Title',
            'content': 'Test Content',
            'secret': 'secret'
        }
        self.assertEqual(result, expected)
        # Verify private attributes are excluded
        self.assertNotIn('_private_attr', result)
        self.assertNotIn('__class__', result)
    
    def test_exclude_fields(self):
        """Test exclude_fields functionality"""
        obj = self.TestModelWithToDict(1, "John Doe", "john@example.com", "secret123")
        result = self.serializer.serializer(obj, exclude_fields=['password', 'email'])
        
        expected = {
            'id': 1,
            'name': 'John Doe'
        }
        self.assertEqual(result, expected)
        self.assertNotIn('password', result)
        self.assertNotIn('email', result)
    
    def test_include_fields(self):
        """Test include_fields functionality (whitelist)"""
        obj = self.TestModelWithToDict(1, "John Doe", "john@example.com", "secret123")
        result = self.serializer.serializer(obj, include_fields=['id', 'name'])
        
        expected = {
            'id': 1,
            'name': 'John Doe'
        }
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 2)
        self.assertNotIn('email', result)
        self.assertNotIn('password', result)
    
    def test_empty_exclude_include(self):
        """Test with empty exclude and include fields"""
        obj = self.TestModelWithToDict(1, "John Doe", "john@example.com", "secret123")
        result = self.serializer.serializer(obj, exclude_fields=[], include_fields=[])
        
        expected = {
            'id': 1,
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'secret123'
        }
        self.assertEqual(result, expected)
    
    def test_none_exclude_include(self):
        """Test with None exclude and include fields"""
        obj = self.TestModelWithToDict(1, "John Doe", "john@example.com", "secret123")
        result = self.serializer.serializer(obj, exclude_fields=None, include_fields=None)
        
        expected = {
            'id': 1,
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'secret123'
        }
        self.assertEqual(result, expected)
    
    def test_callable_attributes_excluded(self):
        """Test that callable attributes are excluded"""
        class TestCallableModel:
            def __init__(self, name: str):
                self.name = name
                self.method = lambda: "should_be_excluded"
            
            def regular_method(self):
                return "should_also_be_excluded"
        
        obj = TestCallableModel("Test")
        result = self.serializer.serializer(obj)
        
        self.assertEqual(result, {'name': 'Test'})
        self.assertNotIn('method', result)
        self.assertNotIn('regular_method', result)
    
    def test_invalid_json_string(self):
        """Test handling of invalid JSON string"""
        class InvalidJSONModel:
            def to_json(self):
                return "invalid json string"
        
        obj = InvalidJSONModel()
        result = self.serializer.serializer(obj)
        
        self.assertEqual(result, {})
    
    def test_multiple_calls_no_data_accumulation(self):
        """Test that serialized data doesn't accumulate between calls"""
        obj1 = self.TestModelWithToDict(1, "John", "john@example.com", "pass1")
        obj2 = self.TestModelWithToDict(2, "Jane", "jane@example.com", "pass2")
        
        result1 = self.serializer.serializer(obj1)
        result2 = self.serializer.serializer(obj2)
        
        # Results should be independent
        self.assertEqual(result1['id'], 1)
        self.assertEqual(result2['id'], 2)
        self.assertNotEqual(result1, result2)
    
    def test_combined_exclude_and_include(self):
        """Test that exclude takes precedence over include"""
        obj = self.TestModelWithToDict(1, "John Doe", "john@example.com", "secret123")
        
        # Even if included, excluded fields should be removed
        result = self.serializer.serializer(
            obj, 
            exclude_fields=['password'],
            include_fields=['id', 'name', 'password']  # password included but should be excluded
        )
        
        expected = {
            'id': 1,
            'name': 'John Doe'
        }
        self.assertEqual(result, expected)
        self.assertNotIn('password', result)

if __name__ == '__main__':
    unittest.main()