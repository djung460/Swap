import bcrypt
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from swapapp.models import Student, Instructor
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def join(request):
    """
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
        print(instructor)

    return HttpResponseRedirect('/login')

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
            return HttpResponseRedirect('/login')

        print(student.pwhash)
        print(bcrypt.hashpw(data['password'].encode('utf-8'), student.pwhash))
        if str(bcrypt.hashpw(data['password'].encode('utf-8'), student.pwhash)) == str(student.pwhash):
            return HttpResponseRedirect('/user/' + student.username)
        else:
            return HttpResponseRedirect('/login')
    else:
        res = Instructor.get(username)
        # assign the tuple
        instructor = Instructor(
            username=res[0],
            pwhash=res[1],
            faculty=res[2],
            email=res[3],
            name=res[4],
            phonenumber=res[5])
        if instructor == None:
            return HttpResponseRedirect('/login')
        if str(bcrypt.hashpw(data['password'].encode('utf-8'), instructor.pwhash)) == str(instructor.pwhash):
            return HttpResponseRedirect('/user/' + instructor.username)
        else:
            return HttpResponseRedirect('/login')
