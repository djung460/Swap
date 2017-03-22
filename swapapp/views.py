from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from .models import Student, Instructor, Equipment, Class


# Create your views here
def index(request):
    return render(request, 'swap/index.html')


def login(request):
    return render(request, 'swap/login.html')


def join(request):
    return render(request, 'swap/join.html')


def search(request):
    return render(request, 'swap/search.html')


def student(request, user=''):
    if request.user.is_authenticated:
        username = request.user.username[1:]
        stud = Student.get(username)
        equiplist = stud.getOwnedEquipment()
        classlist = stud.getEnrolled()
        print(classlist)
        obj = {
            'student': stud,
            'equiplist': equiplist,
            'classlist': classlist
        }
        context = RequestContext(request, {
            'obj': obj
        })
        return render_to_response('swap/student.html', context=context)
    else:
        return HttpResponseRedirect('/')


def addClass(request, user=''):
    """
    View for adding a new class
    """
    if request.user.is_authenticated:
        return render_to_response('swap/instructor_addclass.html')
    else:
        return HttpResponseRedirect('/')


def enroll(request, user=''):
    """
    View for enrolling in a class
    """
    if request.user.is_authenticated:
        classlist = Class.getAll()
        obj = {
            'classlist': classlist
        }

        print(classlist)

        context = RequestContext(request, {
            'obj': obj
        })
        return render_to_response('swap/student_enroll.html', context=context)
    else:
        return HttpResponseRedirect('/')


def addStudentEquipment(request, user=''):
    print("Redirect to add student equipment")
    """
    View for adding an equipment to a student's owned equipment list
    """
    if request.user.is_authenticated:
        username = request.user.username[1:]
        stud = Student.get(username)
        equiplist = Equipment.getAll()
        obj = {
            'equiplist': equiplist
        }

        print(equiplist)

        context = RequestContext(request, {
            'obj': obj
        })
        return render_to_response('swap/student_addequipment.html', context=context)
    else:
        return HttpResponseRedirect('/')


def instructor(request, user=''):
    if request.user.is_authenticated:
        inst = Instructor.get(request.user.username[1:])
        classlist = inst.getClasses()
        obj = {
            'instructor': inst,
            'classlist':classlist
        }
        print(inst.username, classlist)
        context = RequestContext(request, {
            'obj': obj
        })
        return render_to_response('swap/instructor.html', context=context)
    else:
        return HttpResponseRedirect('/')
