from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import random
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from swapapp.models import *


class JSONResponse(HttpResponse):
    """
    HttpResponse that renders its content to JSON
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def user(request):
    return HttpResponse(status=400)


@csrf_exempt
def equipment(request):
    return HttpResponse(status=400)


@csrf_exempt
def searchequipment(request):
    """
    Handles updating an owned equipment from a student
    """
    data = request.POST
    keyword = data['keyword']
    type = data['type']
    faculty = data['faculty']
    classnum = data['classnum']
    min = data['minquantity']
    maxTrades = ConfirmedTrade.getMax()
    maxTradesUser = ConfirmedTrade.getMaxByUser()
    avgTradesUser = ConfirmedTrade.getAvg()
    numUsers = Student.getNum()
    numEquipment = StudentHasEquipment.getNum()
    maxEquipment = StudentHasEquipment.getMaxNum()

    try:
        equiplist = Equipment.updateSearch(keyword=keyword, type=type, faculty=faculty, classnum=classnum, min=min)
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
    except IntegrityError:
        return HttpResponseRedirect('/search')


def equipmentmax(request):
    equiplist = Equipment.getMax()
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


def equipmentmin(request):
    equiplist = Equipment.getMin()
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


@csrf_exempt
def findtrade(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    username = request.user.username[1:]
    user = Student.get(username)
    if request.method == 'GET':
        possibletrades = user.findPossibleTrades()
        # TODO: remove pendingTable trades from possibletrades

        return render(request=request, template_name='swap/student_findpossibletrades.html',
                      context={'pt': possibletrades})
    elif request.method == 'POST':
        """
        Handles adding a pending trade request to the users
        """
        if request.user.is_authenticated:
            username = request.user.username[1:]
            stud = Student.get(username)
            data = request.POST
            trade = data['trade'].split('-')
            print(trade)
            requestequipid = trade[0]
            responseequipid = trade[1]
            responseusername = trade[2]

            possibletrades = user.findPossibleTrades()

            # Check for existing trades between same users with same equipment
            doesExist = PendingTrade.checkExisting(requestusername=username, responseusername=responseusername,
                                                   requestequipid=requestequipid, responseequipid=responseequipid)
            if doesExist:
                error = "Pending trade already exists select another"
                return render(request=request, template_name='swap/student_findpossibletrades.html',
                              context={'pt': possibletrades, 'error': error})
            try:
                stud.addPendingTrade(responseusername=responseusername, requestequipid=requestequipid,
                                     responseequipid=responseequipid)
            except IntegrityError:
                return HttpResponseRedirect('/student/' + username)

            return HttpResponseRedirect('/student/' + username)
        else:
            return HttpResponseRedirect('/')


@csrf_exempt
def trade(request):
    return HttpResponse(status=400)


@csrf_exempt
def course(request):
    return HttpResponse(status=400)


@csrf_exempt
def instructor(request):
    return HttpResponse(status=400)


@csrf_exempt
def addequipment(request):
    return HttpResponse(status=400)
