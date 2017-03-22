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

        equipid = data['equipid']
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