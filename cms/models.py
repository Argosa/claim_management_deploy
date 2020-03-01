from datetime import date, timedelta
from django.db import models
from login_reg.models import User
from patient_reg.models import Patient

# Create your models here.
class ClaimManager(models.Manager):
    def claim_validator(self, postData):
        validator = {
            'isValid': True,
            'errors': {},
        }

        if len(postData['claim_number']) < 5:
            validator['isValid'] = False
            validator['errors']['claim_number'] = 'Claim number must be 5 characters or more'
        if len(postData['claim_issue']) < 10:
            validator['isValid'] = False
            validator['errors']['claim_issue'] = 'Claim issue must be 10 characters or more'
        return validator

    def edit_validator(self, postData):
        validator = {
            'isValid': True,
            'errors': {},
        }

        if len(postData['claim_number']) < 5:
            validator['isValid'] = False
            validator['errors']['claim_number'] = 'Claim number must be 5 characters or more'
        return validator

class ActionManager(models.Manager):
    def action_validator(self, postData):
        validator = {
            'isValid': True,
            'errors': {},
            'follow_up': False,
        }

        if len(postData['note']) < 10:
            validator['isValid'] = False
            validator['errors']['note'] = 'Your note must be at least 10 characters'
        if 'follow_up' in postData:
            validator['follow_up'] = True
            currentDate = date.today()
            followUpDays = int(postData['follow_up_days'])
            followUpDate = currentDate + timedelta(days=followUpDays)
            validator['follow_up_date'] = followUpDate
            print(f"follow up date {validator['follow_up_date']}")
        return validator

class Insurance(models.Model):
    insurance_company = models.CharField(max_length=150)

class ActionType(models.Model):
    type = models.CharField(max_length=100)

class Action(models.Model):
    action = models.ForeignKey(ActionType, related_name='type_of_action', on_delete = models.CASCADE)
    note = models.TextField()
    follow_up = models.BooleanField(default=False)
    follow_up_date = models.DateField()
    user = models.ForeignKey(User, related_name='action_user', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ActionManager()

class Claim(models.Model):
    claim_number = models.CharField(max_length=100)
    patient = models.ForeignKey(Patient, related_name='patient_claim', on_delete = models.CASCADE)
    date_of_service = models.DateField()
    insurance = models.ForeignKey(Insurance, related_name='claim_insurance', on_delete = models.CASCADE)
    issue = models.TextField()
    finished = models.BooleanField()
    follow_up = models.BooleanField(default=False)
    actions = models.ManyToManyField(Action, related_name='claim_action')
    user = models.ForeignKey(User, related_name='user_claim', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ClaimManager()