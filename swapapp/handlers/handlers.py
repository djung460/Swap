from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import random


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
