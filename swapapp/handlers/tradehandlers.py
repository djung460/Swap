from sqlite3 import IntegrityError
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from swapapp.models import Student


@csrf_exempt
def addpending(request):
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

        try:
            stud.addPendingTrade(responseusername=responseusername, requestequipid=requestequipid,
                                 responseequipid=responseequipid)
        except IntegrityError:
            return HttpResponseRedirect('/student/' + username)

        return HttpResponseRedirect('/student/' + username)
    else:
        return HttpResponseRedirect('/')
