import re, bcrypt
from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def reg_validatior(self, postData):
        validator = {
            'isValid': True,
            'errors': {}
        }

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        user = self.filter(email=postData['email'])

        if user:
            validator['errors']['user'] = 'email already exists'
        if len(postData['first_name']) < 2:
            validator['isValid'] = False
            validator['errors']['first_name'] = 'Your first name must be 2 characters or more'
        if len(postData['last_name']) < 2:
            validator['isValid'] = False
            validator['errors']['last_name'] = 'Your last name must be 2 characters or more'
        if not EMAIL_REGEX.match(postData['email']):
            validator['isValid'] = False
            validator['errors']['email'] = 'Please enter a valid email'
        if postData['email'] != postData['confirm_email']:
            validator['isValid'] = False
            validator['errors']['confirm_email'] = 'Your emails must match'
        if len(postData['password']) < 8:
            validator['isValid'] = False
            validator['errors']['password'] = 'Your password must be 8 characters or more'
        if postData['password'] != postData['confirm_password']:
            validator['isValid'] = False
            validator['errors']['confirm_password'] = 'Your password must match'
        return validator

    def login_validator(self, postData):
        validator = {
            'isValid': True,
            'errors': {},
            'user_id': None,
            'isAdmin': False
        }

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        user = self.filter(email=postData['email'])

        if user:
            current_user = user[0]
            if current_user.user_type == 'admin':
                validator['isAdmin'] = True
            print(current_user)
            if not bcrypt.checkpw(postData['password'].encode(), current_user.password.encode()):
                validator['isValid'] = False
                validator['errors']['password'] = 'Your password is incorrect'
                return validator
            else:
                validator['user_id'] = current_user.id
                return validator

        else:
            validator['isValid'] = False
            validator['errors']['email'] = 'Your email was not found'
            return validator

class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()