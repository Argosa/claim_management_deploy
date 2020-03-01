from django.db import models
from login_reg.models  import User

# Create your models here.
class PatientManager(models.Manager):
    def isInt(self, strVar):
        # is a given string an integer
        try: int(strVar)
        except ValueError: return 0
        else:
            return 1 # from python cookbook

    def patient_validator(self, postData):
        validator = {
            'isValid': True,
            'errors': {}
        }

        patient = self.filter(account_number=postData['account_number'])

        if patient:
            validator['isValid'] = False
            validator['errors']['patient'] = 'Account number is already registered'
        if len(postData['first_name']) < 2:
            validator['isValid'] = False
            validator['errors']['first_name'] = 'Patient first name must be 2 characters or more'
        if len(postData['last_name']) < 2:
            validator['isValid'] = False
            validator['errors']['last_name'] = 'Patient last name must be 2 characters or more'
        return validator

    def edit_validator(self, postData):
        validator = {
            'isValid': True,
            'errors': {}
        }

        if len(postData['first_name']) < 2:
            validator['isValid'] = False
            validator['errors']['first_name'] = 'First name must be 2 characters or more'
        if len(postData['last_name']) < 2:
            validator['isValid'] = False
            validator['errors']['last_name'] = 'Last name must be 2 characters or more'
        return validator


class Patient(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    birth_date = models.DateField()
    account_number = models.IntegerField()
    user = models.ForeignKey(User, related_name='patient_user', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PatientManager()