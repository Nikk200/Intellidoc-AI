from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from documents.task import add_numbers

@login_required
def index(request):
    add_numbers.delay(2, 4)
    return render(request, 'index.html')


def register(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('pass')

        user = User.objects.filter(email=email).first()
        if user is not None:
            return HttpResponseBadRequest(f"User with {email} this email address is already registered.")
        else:
            User.objects.create_user(first_name=fname, last_name=lname, email=email, username=email, password=password)
            return HttpResponse("Successfully registered!")
    else:
        return render(request, 'register.html')


def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('pass')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponseBadRequest("User does not exist.")
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return render(request, 'login.html')