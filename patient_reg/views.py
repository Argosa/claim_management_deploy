from django.shortcuts import render, redirect
from login_reg.models import User
from django.contrib import messages
from .models import Patient

# Create your views here.
def register(request):
    if "user_id" not in request.session:
        redirect('/')

    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'all_patients': Patient.objects.all()
    }
    return render(request, 'register.html', context)

def process_patient(request):
    if request.method != 'POST':
        return redirect('patient/')
    
    validator = Patient.objects.patient_validator(request.POST)

    if not validator['isValid']:
        for key, value in validator['errors'].items():
            messages.error(request, value)
            return redirect('patient/')
    else:
        patientFirstName = request.POST['first_name']
        patientLastName = request.POST['last_name']
        patientDob = request.POST['date_of_birth']
        patientAccount = int(request.POST['account_number'])
        patientUser = User.objects.get(id=request.session['user_id'])
        patientVar = f"{patientFirstName} {patientLastName} {patientLastName} {patientDob} {patientAccount}"
        Patient.objects.create(first_name=patientFirstName, last_name=patientLastName, birth_date=patientDob, account_number=patientAccount, user=patientUser)
        print('added to database')
        return redirect('patient/')

def edit_patient(request, myInt):
    if "user_id" not in request.session:
        redirect('/')

    context = {
       'current_user': User.objects.get(id=request.session['user_id']),
       'current_patient': Patient.objects.get(id=myInt) 
    }
    return render(request, 'editpatient.html', context)

def delete_patient(request):
    if request.method != 'POST':
        return redirect('patient/')
    else:
        c = Patient.objects.get(id=int(request.POST['patient_id']))
        c.delete()
        return redirect('patient/')

def go_edit(request):
    if request.method != 'POST':
        return redirect('patient/')
    currentPatientID = request.POST['patient_id']
    return redirect(f"edit_template/{currentPatientID}")

def edit_template(request, myInt):
    if 'user_id' not in request.session:
        redirect('/')

    context = {
       'current_user': User.objects.get(id=request.session['user_id']),
       'current_patient': Patient.objects.get(id=myInt) 
    }
    return render(request, "edittemplate.html", context)

def process_edit(request):
    validator = Patient.objects.edit_validator(request.POST)
    currentPatientID = request.POST['patient_id']

    if not validator['isValid']:
        for key, value in validator['errors'].items():
            messages.error(request, value)
        return redirect(f"edit_template/{currentPatientID}")
    
    c = Patient.objects.get(id=currentPatientID)
    tempFirstName = request.POST['first_name']
    tempLastName = request.POST['last_name']
    tempDob = request.POST['birth_date']
    tempAccountNumber = request.POST['account_number']
    tempVar = f"{tempFirstName} {tempLastName} {tempDob} {tempAccountNumber}"
    
    c.first_name = tempFirstName
    c.last_name = tempLastName
    c.birth_date = tempDob
    c.account_number = tempAccountNumber
    c.save()

    print('database updated')

    return redirect(f"edit_patient/{currentPatientID}")
