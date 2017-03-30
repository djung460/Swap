from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from .models_ubc_courses import COURSES
from .models import *


# Create your views here
def index(request):
    return render(request, 'swap/index.html')


def login(request):
    return render(request, 'swap/login.html')


def join(request):
    return render(request, 'swap/join.html', {
        'coursecodelist': COURSES
    })


def search(request):
    equiplist = Equipment.getAll()
    maxTrades = ConfirmedTrade.getMax()
    maxTradesUser = ConfirmedTrade.getMaxByUser()
    avgTradesUser = ConfirmedTrade.getAvg()
    numUsers = Student.getNum()
    numEquipment = StudentHasEquipment.getNum()
    maxEquipment = StudentHasEquipment.getMaxNum()

    for item in equiplist:
        item['classlist'] = ClassRequiresEquipment.getClasses(str(item['equipmentID']))

    return render(request, 'swap/search.html', {
        'equiplist': equiplist,
        'maxTrades': maxTrades,
        'maxTradesUser': maxTradesUser,
        'avgTradesUser': avgTradesUser,
        'numUsers': numUsers,
        'numEquipment': numEquipment,
        'maxEquipment': maxEquipment
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
    """
    View for adding a new class
    """
    return render(request, 'swap/instructor_addclass.html', {
        'coursecodelist': COURSES
    })


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
    print("Redirect to add student equipment")
    """
    View for adding an equipment to a student's owned equipment list
    """
    if request.user.is_authenticated:
        equiplist = Equipment.getAll()

        return render(request,'swap/student_addequipment.html', {
            'equiplist': equiplist
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

        return render(request,'swap/instructor_addequipment.html',{
            'faculty': faculty,
            'classnum': classnum,
            'term': term,
            'equiplist': equiplist
        })
    else:
        return HttpResponseRedirect('/')
