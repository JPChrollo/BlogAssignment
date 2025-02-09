import unittest
from unittest.mock import patch
from blogapp import app
from blogapp.models import db, User, Post

class BlogAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to My Blog', response.data)

    def test_register_user(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password'
        }
        response = self.app.post('/register', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have successfully registered!', response.data)

    def test_login_user(self):
        self.test_register_user()
        data = {
            'email': 'testuser@example.com',
            'password': 'password'
        }
        response = self.app.post('/login', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are logged in!', response.data)

    def test_create_post(self):
        self.test_login_user()
        data = {
            'title': 'Test Post',
            'content': 'This is a test post.'
        }
        response = self.app.post('/create-post', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post created successfully!', response.data)

    def test_update_post(self):
        self.test_create_post()
        post = Post.query.first()
        data = {
            'title': 'Updated Post',
            'content': 'This post has been updated.'
        }
        response = self.app.post(f'/update-post/{post.id}', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post updated successfully!', response.data)

    def test_delete_post(self):
        self.test_create_post()
        post = Post.query.first()
        response = self.app.get(f'/delete-post/{post.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post deleted successfully!', response.data)

if __name__ == '__main__':
    unittest.main()