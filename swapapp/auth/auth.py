import bcrypt
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from swapapp.models import Student, Instructor
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from django.contrib.auth import login as djangologin
from django.contrib.auth import logout as djangologout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


@csrf_exempt
def join(request):
    """
    Create a django user and a user for the database
    Handles post requests for joins
    """
    data = request.POST

    username = data['username']

    # hash the password
    pwhash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    year = data['year']
    faculty = data['faculty']
    email = data['email']
    name = data['name']
    phonenumber = data['phonenumber']
    print('Join user')
    if data['kind'] == 'student':
        student = Student(
            username=username,
            pwhash=pwhash,
            year=year,
            faculty=faculty,
            email=email,
            name=name,
            phonenumber=phonenumber
        )
        student.insert()
        # Create a django user
        user = User.objects.create_user('s' + username, email, data['password'])
        user.save()
        print(student)
    else:
        instructor = Instructor(
            username=username,
            pwhash=pwhash,
            faculty=faculty,
            email=email,
            name=name,
            phonenumber=phonenumber
        )
        instructor.insert()
        # Create a django user
        user = User.objects.create_user('i' + username, email, data['password'])
        user.save()
        print(instructor)

    return HttpResponseRedirect('/login')

def logout(request):
    """
    Handles logging out the user
    """
    djangologout(request)
    print('LOGOUT')
    return HttpResponseRedirect('/')

@csrf_exempt
def login(request):
    """
    Handles put requests for logins
    """

    data = request.POST

    username = data['username']

    print(data['kind'])

    if data['kind'] == 'student':
        res = Student.get(username)

        user = authenticate(username='s' + data['username'], password=data['password'])

        print(user)

        if user is not None:

            djangologin(request, user)
            return HttpResponseRedirect('/student/' + res.username)
        else:
            return HttpResponseRedirect('/login')
    else:
        res = Instructor.get(username)

        user = authenticate(username='i' + data['username'], password=data['password'])

        if user is not None:
            djangologin(request, user)
            return HttpResponseRedirect('/instructor/' + res.username)
        else:
            return HttpResponseRedirect('/login')
