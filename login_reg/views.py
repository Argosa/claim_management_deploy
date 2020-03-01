import bcrypt
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    return render(request, 'logindash.html')

def process_reg(request):
    # make sure the method is post and if not redirect
    if request.method != 'POST':
        return redirect('/')

    validator = User.objects.reg_validatior(request.POST)
    # set validator for registration to variable validator

    if not validator['isValid']:
        # if the errors dictionary contains errors loop through it
        for key, value in validator['errors'].items():
            messages.error(request, value)
        # if errors exist redirect
        return redirect('/')
    else:
        #if there were no errors proceed ...
        tempFirstName = request.POST['first_name']
        tempLastName = request.POST['last_name']
        tempEmail = request.POST['email']
        tempPassword = request.POST['password']
        tempHash = bcrypt.hashpw(tempPassword.encode(), bcrypt.gensalt()).decode()
        tempVar = f"{tempFirstName} {tempLastName} {tempEmail} {tempPassword} {tempHash}"
        print(tempVar)
        newUser = User.objects.create(first_name=tempFirstName, last_name=tempLastName, email=tempEmail, password=tempHash)
        request.session['user_id'] = newUser.id
        return redirect('/success')

def process_login(request):
    if request.method != "POST":
        return redirect('/')
    
    validator = User.objects.login_validator(request.POST)

    if not validator['isValid']:
        for key, value in validator['errors'].items():
            messages.error(request, value)
            return redirect('/')
    else:
        request.session['user_id'] = validator['user_id']
        if validator['isAdmin']:
            request.session['isAdmin'] = True
        if request.POST['destination'] == 'patient':
            return redirect('patient/')
        else:
            return redirect('claim_dashboard/')


def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'success.html', context)