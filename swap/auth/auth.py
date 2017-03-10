import bcrypt
from django.http import HttpResponse
from django.db import connection
from swap.models import Student
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def join(request):
    """
    Handles put requests for joins
    """

    data = JSONParser().parse(request)

    username = data['username']

    # check to see if a username is already in the database
    userexist = Student.objects.filter(username=username).exists()

    # hash the password
    pwhash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    if userexist:
        return HttpResponse(status=401)

    year = data['year']
    faculty = data['faculty']
    email = data['email']
    name = data['name']
    phonenumber = data['phonenumber']

    student = Student(
        username=username,
        pwhash=pwhash,
        year=year,
        faculty=faculty,
        email=email,
        name=name,
        phonenumber=phonenumber)

    student.insert()

    return HttpResponse(status=201)

def login(request):
    """
    Handles put requests for logins
    """

    return HttpResponse(status=401)
