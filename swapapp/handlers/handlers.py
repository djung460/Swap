from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import random
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from swapapp.models import Equipment


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
    type =  data['type']
    faculty = data['faculty']
    classnum = data['classnum']
    min = data['minquantity']

    try:
        equiplist = Equipment.updateSearch(keyword=keyword,type=type, faculty=faculty, classnum=classnum, min=min)
        return render(request, 'swap/search.html', {
            'equiplist': equiplist,
        })
    except IntegrityError:
        return HttpResponseRedirect('/search')

def equipmentmax(request):
    equiplist = Equipment.getMax()
    return render(request, 'swap/search.html', {
        'equiplist': equiplist,
    })

def equipmentmin(request):
    equiplist = Equipment.getMin()
    return render(request, 'swap/search.html', {
        'equiplist': equiplist,
    })

def equipmentavg(request):
    equiplist = Equipment.getAvg()
    return render(request, 'swap/search.html', {
        'equiplist': equiplist,
    })

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
