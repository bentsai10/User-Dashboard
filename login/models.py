from django.db import models
import bcrypt
import re

# Create your models here.

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters!"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        if postData['password'] != postData['password_conf']:
            errors['password'] = "Your passwords don't match!"
        
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        user = User.objects.filter(email=postData['email']) 
        if user:
            logged_user = user[0] 
            if not bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                errors["password"] = "Incorrect password!"
        else:
            errors["email"] = "This email has not been registered!"
        return errors
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    user_level = models.IntegerField()
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()