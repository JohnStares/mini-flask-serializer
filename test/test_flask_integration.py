# test_flask_integration.py
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# I installed the package in development mode to test it out here
from mini_flask_serializer import MiniFlaskSerializer

class TestFlaskSQLAlchemyIntegration(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        self.db = SQLAlchemy(self.app)
        self.serializer = MiniFlaskSerializer()
        
        # Create test model
        class User(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            username = self.db.Column(self.db.String(80), unique=True)
            email = self.db.Column(self.db.String(120))
            password_hash = self.db.Column(self.db.String(128))
            
            def to_dict(self):
                return {
                    'id': self.id,
                    'username': self.username,
                    'email': self.email
                }
        
        self.User = User
        
        with self.app.app_context():
            self.db.create_all()
            user = User(username='testuser', email='test@example.com', password_hash='hashed')
            self.db.session.add(user)
            self.db.session.commit()
    
    def tearDown(self):
        """Clean up database connections after each test"""
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
            self.db.engine.dispose()
    
    def test_flask_sqlalchemy_model(self):
        """Test serialization with actual Flask-SQLAlchemy model"""
        with self.app.app_context():
            user = self.User.query.first()
            result = self.serializer.serializer(user)
            
            expected = {
                'id': 1,
                'username': 'testuser',
                'email': 'test@example.com'
            }
            self.assertEqual(result, expected)
            self.assertNotIn('password_hash', result)
    
    def test_flask_sqlalchemy_with_exclude(self):
        """Test exclude_fields with Flask-SQLAlchemy model"""
        with self.app.app_context():
            user = self.User.query.first()
            result = self.serializer.serializer(user, exclude_fields=['email'])
            
            expected = {
                'id': 1,
                'username': 'testuser'
            }
            self.assertEqual(result, expected)
    
    def test_flask_sqlalchemy_with_include(self):
        """Test include_fields with Flask-SQLAlchemy model"""
        with self.app.app_context():
            user = self.User.query.first()
            result = self.serializer.serializer(user, include_fields=['id', 'username'])
            
            expected = {
                'id': 1,
                'username': 'testuser'
            }
            self.assertEqual(result, expected)
            self.assertNotIn('email', result)
    
    def test_flask_sqlalchemy_direct_attributes(self):
        """Test serialization without to_dict method (direct attribute access)"""
        with self.app.app_context():
            user = self.User.query.first()
            
            # Create a simple object without to_dict method to test fallback
            class SimpleObject:
                def __init__(self, id, name, secret):
                    self.id = id
                    self.name = name
                    self._secret = secret
                    self.method = lambda: "should_be_excluded"
            
            simple_obj = SimpleObject(1, "test", "secret_value")
            result = self.serializer.serializer(simple_obj)
            
            # Should include public attributes, exclude private and callable
            self.assertEqual(result['id'], 1)
            self.assertEqual(result['name'], 'test')
            self.assertNotIn('_secret', result)
            self.assertNotIn('method', result)
    
    def test_flask_sqlalchemy_with_both_filters(self):
        """Test combining exclude and include fields"""
        with self.app.app_context():
            user = self.User.query.first()
            
            # Exclude should take precedence over include
            result = self.serializer.serializer(
                user, 
                exclude_fields=['email'],
                include_fields=['id', 'username', 'email']  # email included but should be excluded
            )
            
            expected = {
                'id': 1,
                'username': 'testuser'
            }
            self.assertEqual(result, expected)
            self.assertNotIn('email', result)

if __name__ == '__main__':
    unittest.main()