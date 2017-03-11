import bcrypt
from django.http import HttpResponse
from django.db import connection
from swapapp.models import Student
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

@csrf_exempt
def login(request):
    """
    Handles put requests for logins
    """
    data = JSONParser().parse(request)

    username = data['username']

    res = Student.get(username)
    # assign the tuple
    student = Student(
            username=res[0],
            pwhash=res[1],
            year=res[2],
            faculty=res[3],
            email=res[4],
            name=res[5],
            phonenumber=res[6])


    if student == None:
        return HttpResponse(201)

    if bcrypt.hashpw(data['password'].encode('utf-8'),student.pwhash)==student.pwhash:
        return HttpResponse(201)
    else:
        return HttpResponse(400)
