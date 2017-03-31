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
def addequipment(request):
    """
    Handles adding a required equipment to a class
    """
    if request.user.is_authenticated:
        username = request.user.username[1:]
        inst = Instructor.get(username)

        data = request.POST

        classinfo = data['class'].split('-')
        print(classinfo)
        faculty = classinfo[0]
        classnum = classinfo[1]
        term = classinfo[2]

        equipid = data['kind']

        try:
            inst.addEquipToClass(faculty=faculty,classnum=classnum,term=term,equipid=equipid)
        except IntegrityError:
            print("Equipment already added to class")
            HttpResponseRedirect('/overview/class/' + faculty + '-' + classnum + '-' + term)
        print("Equipment succesfully added")
        return HttpResponseRedirect('/overview/class/' + faculty + '-' + classnum + '-' + term)
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def deleteequipment(request):
    """
    Handles adding a required equipment to a class
    """
    if request.user.is_authenticated:
        username = request.user.username[1:]
        inst = Instructor.get(username)

        data = request.POST

        faculty = data['faculty']
        classnum = data['classnum']
        term = data['term']
        equipid = data['equipid']

        try:
            inst.deleteEquipFromClass(faculty=faculty,classnum=classnum,term=term,equipid=equipid)
        except IntegrityError:
            print("Equipment already added to class")
            HttpResponseRedirect('/overview/class/' + faculty + '-' + classnum + '-' + term)
        print("Equipment succesfully added")
        return HttpResponseRedirect('/overview/class/' + faculty + '-' + classnum + '-' + term)
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def deleteclass(request):
    """
    Handles deleting a class, cascades
    """
    if request.user.is_authenticated:
        username = request.user.username[1:]
        inst = Instructor.get(username)

        data = request.POST

        faculty = data['faculty']
        classnum = data['classnum']
        term = data['term']

        print(faculty, classnum, term)

        try:
            inst.deleteClass(faculty=faculty, classnum=classnum, term=term)
        except IntegrityError:
            print("Class already exists")
            return HttpResponseRedirect('/instructor/' + username)

        print("Class deleted")
        return HttpResponseRedirect('/instructor/' + username)
    else:
        return HttpResponseRedirect('/')