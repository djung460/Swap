from sqlite3 import IntegrityError

import bcrypt
import re
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from swapapp.auth import auth
from .models_ubc_courses import COURSES
from .models_ubc_courses import TERMS
from .models import *


# Create your views here
def index(request):
    return render(request, 'swap/index.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'swap/login.html')
    else:
        return auth.login(request)


def join(request):
    if request.method == 'GET':
        return render(request, 'swap/join.html', {
            'coursecodelist': COURSES
        })
    else:
        """
        Create a django user and a user for the database
        Handles post requests for joins
        """
        data = request.POST

        username = data['username']

        # hash the password
        pwhash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        faculty = data['faculty']
        email = data['email']

        haserror = False
        phonenumbererror = ''
        usernameerror = ''
        emailerror = ''


        if '@' not in str(email):
            haserror = True
            emailerror = "Invalid email"

        name = data['name']
        phonenumber = data['phonenumber']

        phonePattern = re.compile(r'^(\d{3})-(\d{3})-(\d{4})$')

        if not phonePattern.match(phonenumber):
            haserror = True
            phonenumbererror = "Invalid phone number"

        print('Join user')

        if data['kind'] == 'student' and not haserror:

            # Only student accounts have a year
            year = data['year']

            student = Student(
                username=username,
                pwhash=pwhash,
                year=year,
                faculty=faculty,
                email=email,
                name=name,
                phonenumber=phonenumber
            )
            try:
                student.insert()
                # Create a django user
                user = User.objects.create_user('s' + username, email, data['password'])
                user.save()
                print(student)
            except Exception:
                haserror = True
                usernameerror = "Student username taken!"
        elif data['kind'] != 'student' and not haserror:
            instructor = Instructor(
                username=username,
                pwhash=pwhash,
                faculty=faculty,
                email=email,
                name=name,
                phonenumber=phonenumber
            )
            try:
                instructor.insert()
                # Create a django user
                user = User.objects.create_user('i' + username, email, data['password'])
                user.save()
                print(instructor)
            except Exception:
                haserror = True
                usernameerror = "Instructor username taken!"

        if haserror:
            return render(request, 'swap/join.html', {
                'coursecodelist': COURSES,
                'error_username': usernameerror,
                'error_phonenumber': phonenumbererror,
                'error_email': emailerror
            })
        else:
            return HttpResponseRedirect('/login')


def search(request):
    equiplist = Equipment.getAll()
    maxTrades = ConfirmedTrade.getMax()
    maxTradesUser = ConfirmedTrade.getMaxByUser()
    avgTradesUser = ConfirmedTrade.getAvg()
    numUsers = Student.getNum()
    numEquipment = StudentHasEquipment.getNum()
    maxEquipment = StudentHasEquipment.getMaxNum()
    type = Equipment.getTypes()
    faculty = Class.getFaculties()

    for item in equiplist:
        item['classlist'] = ClassRequiresEquipment.getClasses(str(item['equipmentID']))

    return render(request, 'swap/search.html', {
        'equiplist': equiplist,
        'maxTrades': maxTrades,
        'maxTradesUser': maxTradesUser,
        'avgTradesUser': avgTradesUser,
        'numUsers': numUsers,
        'numEquipment': numEquipment,
        'maxEquipment': maxEquipment,
        'type': type,
        'faculty': faculty
    })


def student(request, user=''):
    if request.user.is_authenticated:
        username = request.user.username[1:]
        stud = Student.get(username)
        equiplist = stud.getOwnedEquipment()
        classlist = stud.getEnrolled()
        requestlist = stud.getPendingTrades(type='request')
        responselist = stud.getPendingTrades(type='response')
        print(classlist)

        for item in classlist:
            item['equiplist'] = ClassRequiresEquipment.get(faculty=item['faculty'], classnum=item['classNum'],
                                                           term=item['term'])
            print(item['equiplist'])

        return render(request, 'swap/student.html', {
            'student': stud,
            'equiplist': equiplist,
            'classlist': classlist,
            'requestlist': requestlist,
            'responselist': responselist
        })

    else:
        return HttpResponseRedirect('/')


def addclass(request, user=''):
    if request.user.is_authenticated:
        if request.method == 'GET':
            """
            View for adding a new class
            """
            return render(request, 'swap/instructor_addclass.html', {
                'coursecodelist': COURSES,
                'terms': TERMS
            })
        elif request.method == 'POST':
            if request.user.is_authenticated:
                username = request.user.username[1:]
                inst = Instructor.get(username)

                data = request.POST

                faculty = data['faculty']
                classnum = data['classnum']
                term = data['term']

                try:
                    inst.addCourse(faculty, classnum, term)
                except Exception:
                    print("Class already exists")
                    error = "Class already exists!"
                    return render(request, 'swap/instructor_addclass.html', {
                        'coursecodelist': COURSES,
                        'terms': TERMS,
                        'error': error
                    })

                success = "Class added succesfully!"
                return render(request, 'swap/instructor_addclass.html', {
                    'coursecodelist': COURSES,
                    'terms': TERMS,
                    'success': success
                })
            else:
                return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def tradehistory(request, user=''):
    if request.user.is_authenticated:
        username = request.user.username[1:]
        stud = Student.get(username)
        requestlist = stud.getConfirmedTrades(type='request')
        responselist = stud.getConfirmedTrades(type='response')

        return render(request, 'swap/tradehistory.html', {
            'student': stud,
            'requestlist': requestlist,
            'responselist': responselist
        })

    else:
        return HttpResponseRedirect('/')


def enroll(request, user=''):
    """
    View for enrolling in a class
    """
    if request.user.is_authenticated:
        classlist = Class.getAll()

        return render(request, 'swap/student_enroll.html', {
            'classlist': classlist
        })
    else:
        return HttpResponseRedirect('/')


def addStudentEquipment(request, user=''):
    if request.method == 'GET':
        print("Redirect to add student equipment")
        """
        View for adding an equipment to a student's owned equipment list
        """
        if request.user.is_authenticated:
            equiplist = Equipment.getAll()

            return render(request, 'swap/student_addequipment.html', {
                'equiplist': equiplist
            })
        else:
            return HttpResponseRedirect('/')
    else:
        if request.user.is_authenticated:
            username = request.user.username[1:]
            stud = Student.get(username)

            data = request.POST

            equiplist = Equipment.getAll()

            equipid = data['kind']
            quantity = data['quantity']
            try:
                stud.addOwnEquipment(equipmentid=equipid, quantity=quantity)
            except Exception:
                print("student already has item")
                error = "You already own this item!"
                return render(request, 'swap/student_addequipment.html', {
                    'equiplist': equiplist,
                    'error': error
                })

            success = "Added succesfully!"
            return render(request, 'swap/student_addequipment.html', {
                'equiplist': equiplist,
                'success': success
            })
        else:
            return HttpResponseRedirect('/')


def instructor(request, user=''):
    if request.user.is_authenticated:
        inst = Instructor.get(request.user.username[1:])
        classlist = inst.getClasses()

        print(inst.username, classlist)

        classlist = inst.getClasses()

        print(inst.username, classlist)
        # Add on the required equipment for each class

        for item in classlist:
            item['equiplist'] = ClassRequiresEquipment.get(faculty=item['faculty'], classnum=item['classNum'],
                                                           term=item['term'])
            print(item['equiplist'])

        return render(request, 'swap/instructor.html', {
            'instructor': inst,
            'classlist': classlist
        })
    else:
        return HttpResponseRedirect('/')


def classoverview(request, faculty='', classnum='', term=''):
    if request.user.is_authenticated:
        inst = Instructor.get(request.user.username[1:])

        hasallequip = inst.getStudentsWithAllEquipment(faculty=faculty, classnum=classnum, term=term)
        equiplist = ClassRequiresEquipment.get(faculty, classnum, term)
        enrolled = StudentTakesClass.getEnrolled(faculty, classnum, term)
        return render(request, 'swap/classoverview.html', {
            'hasallequip': hasallequip,
            'equiplist': equiplist,
            'faculty': faculty,
            'enrolled': enrolled,
            'classnum': classnum,
            'term': term
        })
    else:
        return HttpResponseRedirect('/')


def instructor_addequip(request, faculty='', classnum='', term=''):
    if request.user.is_authenticated:
        equiplist = Equipment.getAll()

        if request.method == 'GET':
            return render(request, 'swap/instructor_addequipment.html', {
                'faculty': faculty,
                'classnum': classnum,
                'term': term,
                'equiplist': equiplist
            })
        elif request.method == 'POST':
            username = request.user.username[1:]
            inst = Instructor.get(username)

            data = request.POST

            classinfo = data['class'].split('-')
            print(classinfo)
            faculty = classinfo[0]
            classnum = classinfo[1]
            term = classinfo[2]

            equipid = data['equipid']

            try:
                inst.addEquipToClass(faculty=faculty, classnum=classnum, term=term, equipid=equipid)
            except Exception:
                print("Equipment already added to class")
                error = "Equipment already added to class!"
                return render(request, 'swap/instructor_addequipment.html', {
                    'faculty': faculty,
                    'classnum': classnum,
                    'term': term,
                    'equiplist': equiplist,
                    'error': error
                })
            print("Equipment succesfully added")
            success = "Equipment succesfully added"
            return render(request, 'swap/instructor_addequipment.html', {
                'faculty': faculty,
                'classnum': classnum,
                'term': term,
                'equiplist': equiplist,
                'success': success
            })

    else:
        return HttpResponseRedirect('/')
