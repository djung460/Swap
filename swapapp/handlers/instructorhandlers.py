from swapapp.models import StudentHasEquipment, Student, Instructor
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError


@csrf_exempt
def addclass(request):
    """
    Handles adding a class
    """
    if request.user.is_authenticated:
        username = request.user.username[1:]
        inst = Instructor.get(username)

        data = request.POST

        faculty = data['faculty']
        classnum = data['classnum']
        term = data['term']

        try:
            inst.addCourse(faculty, classnum, term)
        except IntegrityError:
            print("Class already exists")
            return HttpResponseRedirect('/instructor/' + username)

        return HttpResponseRedirect('/instructor/' + username)
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def enroll(request):
    """
    Handles enrolling in a class
    """
    if request.user.is_authenticated:
        username = request.user.username[1:]
        stud = Student.get(username)

        data = request.POST

        faculty = data['class'][0:4]
        classnum = data['class'][4:7]
        term = data['class'][7:14]

        print(faculty, classnum, term)

        try:
            stud.enroll(faculty=faculty, classnum=classnum, term=term)
        except IntegrityError:
            print("student already has item")
            return HttpResponseRedirect('/student/' + username)


        return HttpResponseRedirect('/student/' + username)
    else:
        return HttpResponseRedirect('/')