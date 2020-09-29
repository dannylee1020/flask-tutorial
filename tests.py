from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_password_hashing(self):
        u = User(username = 'dannylee')
        u.set_password('test')
        self.assertFalse(u.check_password('not_test'))
        self.assertTrue(u.check_password('test'))

    def test_avatar(self):
        u = User(username = 'dannylee', email = 'test@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar55502f40dc8b7c769880b10874abc9d0?d=identicon&s=128'))
    
    def test_follow(self):
        u1 = User(username = 'Danny', email = 'dannylee1@example.com')
        u2 = User(username = 'Sunny', email = 'sunnychung@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u2.followed.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'Sunny')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'Danny')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)
    
    def test_follow_posts(self):
        u1 = User(username = 'Danny', email = 'danny@example.com')
        u2 = User(username = 'Sunny', email = 'sunny@example.com')
        u3 = User(username = 'Leo', email = 'leo@example.com')
        u4 = User(username = 'Andy', email = 'andy@example.com')
        db.session.add_all([u1,u2,u3,u4])

        now = datetime.utcnow()
        p1 = Post(body = 'post from Danny', author = u1, timestamp = now + timedelta(seconds = 1))
        p2 = Post(body= 'post from Sunny', author = u2, timestamp = now + timedelta(seconds = 4))
        p3 = Post(body = 'post from Leo', author = u3, timestamp = now + timedelta(seconds = 3))
        p4 = Post(body = 'post from Andy', author =u4, timestamp = now + timedelta(seconds = 2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        u1.follow(u2) # danny follows sunny
        u1.follow(u4) # danny follows andy
        u2.follow(u3) # sunny follows leo
        u3.follow(u4) # leo follows andy
        db.session.commit()

        f1 = u1.followed_post().all()
        f2 = u2.followed_post().all()
        f3 = u3.followed_post().all()
        f4 = u4.followed_post().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)





        
