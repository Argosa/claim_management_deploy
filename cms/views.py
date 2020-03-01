from django.shortcuts import render, redirect
from django.contrib import messages
from patient_reg.models import Patient
from login_reg.models import User
from .models import Claim, Insurance, Action, ActionType
from datetime import date, timedelta

# Create your views here.
def create_claim(request):
    if request.method != 'POST':
        return redirect('/')
    request.session['patient_id'] = request.POST['patient_id']
    return redirect('claim_entry/')

def claim_entry(request):
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'current_patient': Patient.objects.get(id=request.session['patient_id']),
        'all_insurance': Insurance.objects.all(),
    }
    return render(request, "claim-entry.html", context)

def claim_dashboard(request):
    if 'user_id' not in request.session:
        request.session.clear()
        return redirect ('/')
    currentUser = User.objects.get(id=request.session['user_id'])
    allActions = Action.objects.filter(user=currentUser, follow_up=True)
    allClaims = Claim.objects.filter(user=currentUser, follow_up=True)
    context = {
        'current_user': currentUser,
        'all_claims': allClaims,
        'all_actions': allActions,
    }
    return render(request, 'claim_dashboard.html', context)

def process_claim(request):
    if request.method != 'POST':
        return redirect('claim_dashboard')
        
    validator = Claim.objects.claim_validator(request.POST)

    if not validator['isValid']:
        for key, value in validator['errors'].items():
            messages.error(request, value)
        return redirect('claim_entry/')
    
    claimIssue = request.POST['claim_issue']
    claimPatient = Patient.objects.get(id=request.session['patient_id'])
    claimUser = User.objects.get(id=request.session['user_id'])
    claimNumber = request.POST['claim_number']
    claimDos = request.POST['date_of_service']
    claimInsurance = Insurance.objects.get(id=request.POST['insurance'])
    
    testVar = f"claim number: {claimNumber} date of service: {claimDos} claim issue {claimIssue}"

    newClaim = Claim.objects.create(claim_number=claimNumber, patient=claimPatient, date_of_service=claimDos, insurance=claimInsurance, issue=claimIssue, finished=False, user=claimUser)

    print(testVar)
    return redirect(f"view_claim/{newClaim.id}")

def view_claim(request, myInt):
    viewClaim = Claim.objects.get(id=myInt)
    request.session['patient_id'] = viewClaim.patient.id
    request.session['claim_id'] = viewClaim.id
    currentUser = User.objects.get(id=request.session['user_id'])
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'my_claim': viewClaim,
        'my_actions': viewClaim.actions.all(),
        'all_action_types': ActionType.objects.all(),
        "all_actions": Action.objects.all(),
        'user_type': currentUser.user_type,
    }
    return render(request, 'view_claim.html', context)

def go_view_action(request):
    if request.method != 'POST':
        return redirect('/')
    
    currentClaim = Claim.objects.get(id=request.POST['claim_id'])
    currentPatient = Patient.objects.get(id=request.POST['patient_id'])

    request.session['patient_id'] = currentPatient.id
    request.session['claim_id'] = currentClaim.id

    return redirect(f"view_action/{request.POST['action_id']}")

def process_action(request):
    validator = Action.objects.action_validator(request.POST)

    if not validator['isValid']:
        for key, value in validator['errors'].items():
            messages.error(request, value)
    
    currentUser = User.objects.get(id=request.session['user_id'])
    currentClaim = Claim.objects.get(id=request.POST['claim_id'])
    currentActionType = ActionType.objects.get(id=request.POST['action_type'])
    currentNote = request.POST['note']
    amendedNote = f"Original Note: {currentNote} User: {currentUser.first_name} {currentUser.last_name} Date {date.today()}"

    if 'follow_up' not in request.POST:
        currentFollowUp = False
        currentFollowUpDate = date.today()
    else:
        currentFollowUp = True
        currentFollowUpDate = validator['follow_up_date']
        currentClaim.follow_up = True
        currentClaim.save()

    testVar = f"{currentUser.first_name} {currentClaim.claim_number} {currentActionType} {currentNote} {currentFollowUpDate} {currentFollowUp}"
    print(testVar)
    newAction = Action.objects.create(action=currentActionType, note=amendedNote, follow_up=currentFollowUp, follow_up_date=currentFollowUpDate, user=currentUser)
    print('Action wrote to db yo!')
    currentClaim.actions.add(newAction)
    print('Action added to claim')
    return redirect(f"view_claim/{request.POST['claim_id']}")

def view_action (request, myInt):
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'current_action': Action.objects.get(id=myInt),
        'current_patient': Patient.objects.get(id=request.session['patient_id']),
        'current_claim': Claim.objects.get(id=request.session['claim_id']),
    }
    return render(request, 'view_action.html', context)

def change_follow(request):
    if request.method != 'POST':
        return redirect(f"view_action/{currentAction.id}")
    
    currentUser = User.objects.get(id=request.session['user_id'])
    currentClaim = Claim.objects.get(id=request.POST['claim_id'])
    currentAction = Action.objects.get(id=request.POST['action_id'])
    addFollowUp = int(request.POST['follow_up_days'])
    currentFollowUpDate = currentAction.follow_up_date
    newFollowUpDate = currentFollowUpDate + timedelta(days=addFollowUp)
    currentAction.follow_up_date = newFollowUpDate
    currentAction.follow_up = True
    currentAction.save()
    return redirect(f"view_action/{currentAction.id}")

def close_action(request):
    currentUser = User.objects.get(id=request.session['user_id'])
    currentClaim = Claim.objects.get(id=request.POST['claim_id'])
    currentAction = Action.objects.get(id=request.POST['action_id'])
    currentAction.follow_up = False
    currentAction.follow_up_date = date.today()
    currentAction.save()
    return redirect(f"view_action/{currentAction.id}")

def edit_claim(request, myInt):
    if request.method != 'POST':
        return redirect(f"view_claim/{request.POST['claim_id']}")
    
    currentClaim = Claim.objects.get(id=request.POST['claim_id'])
    currentUser = User.objects.get(id=request.session['user_id'])
    currentPatient = Patient.objects.get(id=request.POST['patient_id'])

    context = {
        'my_claim': currentClaim,
        'current_patient': currentPatient,
        'all_insurance': Insurance.objects.all(),
        'date': str(currentClaim.date_of_service),
    }
    return render(request, 'editclaim.html', context)

def process_claim_edit(request):
    if request.method != 'POST':
        return redirect(f"view_claim/{request.POST['claim_id']}")
    
    validator = Claim.objects.edit_validator(request.POST)

    if not validator['isValid']:
        for key, value in validator['errors'].items():
            messages.error(request, value)
        return redirect(f"view_claim/{request.POST['claim_id']}")

    currentClaim = Claim.objects.get(id=request.POST['claim_id'])
    
    return redirect(f"view_claim/{request.POST['claim_id']}")

def add_action_note(request):
    if request.method != 'POST':
        return redirect(f"view_action/{request.POST['action_id']}")
    
    currentAction = Action.objects.get(id=request.POST['action_id'])
    currentUser = User.objects.get(id=request.session['user_id'])
    currentNote = currentAction.note
    noteAddition = request.POST['note']
    currentDate = date.today()
    newNote = f"{currentNote} Note Addition: {noteAddition} User: {currentUser.first_name} {currentUser.last_name} Date: {currentDate}"
    currentAction.note = newNote
    currentAction.save()
    return redirect(f"view_action/{request.POST['action_id']}")

def delete_claim(request):
    if request.method != 'POST':
        request.session.clear()
        return redirect('/')
    claimId = request.POST['claim_id']
    if 'isAdmin' in request.session:
        if request.POST['delete_text'] == 'DELETE' and 'delete_check' in request.POST:
            print("claim has been deleted")
        else:
            print('claim has not been deleted')
        return redirect('claim_dashboard/')
    else:
        return redirect(f'view_claim/{claimId}')
