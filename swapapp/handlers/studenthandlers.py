from swapapp.models import StudentHasEquipment, Student
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError

@csrf_exempt
def addequipment(request):
    """
    Handles adding an equipment
    """
    if request.user.is_authenticated:
        username = request.user.username[1:]
        stud = Student.get(username)

        data = request.POST

        equipid = data['kind']
        quantity = data['quantity']
        try:
            stud.addOwnEquipment(equipmentid=equipid, quantity=quantity)
        except IntegrityError:
            print("student already has item")
            return HttpResponseRedirect('/student/' + username)


        return HttpResponseRedirect('/student/' + username)
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def deleteequipment(request):
    """
    Handles removing an owned equipment from a student
    """
    if request.user.is_authenticated:
        username = request.user.username[1:]
        stud = Student.get(username)

        data = request.POST

        equipmentid = data['equipmentid']

        try:
            stud.removeEquipment(equipmentid=equipmentid)
        except IntegrityError:
            print("student already has item")
            return HttpResponseRedirect('/student/' + username)


        return HttpResponseRedirect('/student/' + username)
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def updateequipment(request):
    """
    Handles updating an owned equipment from a student
    """
    if request.user.is_authenticated:
        username = request.user.username[1:]
        stud = Student.get(username)

        data = request.POST

        equipmentid = data['equipmentid']
        quantity = data['quantity']
        #tradeable = data['tradeable']

        checkbox = request.POST.get('tradeable', False)

        print('checkbox: ', checkbox=='on')

        if checkbox =='on':
            tradeable = 1
        else:
            tradeable = 0

        try:
            stud.updateOwnedEquipment(equipmentid=equipmentid,quantity=quantity,tradeable=tradeable)
        except IntegrityError:
            return HttpResponseRedirect('/student/' + username)


        return HttpResponseRedirect('/student/' + username)
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

        classinfo = data['class'].split('-')
        print(classinfo)
        faculty = classinfo[0]
        classnum = classinfo[1]
        term = classinfo[2]

        print(faculty, classnum, term)

        try:
            stud.enroll(faculty=faculty, classnum=classnum, term=term)
        except IntegrityError:
            print("student already taking class")
            return HttpResponseRedirect('/student/' + username)


        return HttpResponseRedirect('/student/' + username)
    else:
        return HttpResponseRedirect('/')

@csrf_exempt
def drop(request):
    """
    Handles removing a class
    """
    if request.user.is_authenticated:
        username = request.user.username[1:]
        stud = Student.get(username)

        data = request.POST

        print("Dropping class")

        faculty = data['faculty']
        classnum = data['classnum']
        term = data['term']

        try:
            stud.drop(faculty=faculty, classnum=classnum, term=term)
        except IntegrityError:
            return HttpResponseRedirect('/student/' + username)


        return HttpResponseRedirect('/student/' + username)
    else:
        return HttpResponseRedirect('/')