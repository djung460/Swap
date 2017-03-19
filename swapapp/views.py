from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here
def index(request):
    return render(request, 'swap/index.html')
def login(request):
    return render(request, 'swap/login.html')
def join(request):
    return render(request, 'swap/join.html')
def user(request, user=''):
    if request.user.is_authenticated:
        return render(request, 'swap/user.html')
    else:
        return HttpResponseRedirect('/')

