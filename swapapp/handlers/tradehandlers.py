from sqlite3 import IntegrityError
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from swapapp.models import Student, ConfirmedTrade, PendingTrade, StudentHasEquipment


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


@csrf_exempt
def cancel(request):
    """
    Handles canceling a pending trade
    """
    if request.user.is_authenticated:
        username = request.user.username[1:]
        stud = Student.get(username)

        data = request.POST
        tradeid = data['tradeid']

        try:
            PendingTrade.remove(pendingtradeid=tradeid)
        except IntegrityError:
            return HttpResponseRedirect('/student/' + username)

        return HttpResponseRedirect('/student/' + username)
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def confirm(request):
    """
    Handles confirming a pending trade request
    """
    if request.user.is_authenticated:
        username = request.user.username[1:]
        stud = Student.get(username)

        data = request.POST
        tradeid = data['tradeid']
        by = data['by']

        # Check if the requester or responder confirmed trade occurred
        try:
            if by == 'request':
                # Requester confirmed trade
                res = stud.updatePendingTrade(tradeid=tradeid, requestconfirm=1)
            else:
                # Responder confirmed trade
                res = stud.updatePendingTrade(tradeid=tradeid, responseconfirm=1)

            print("Updated pending trade ", res)
            res = res[0]
            if int(res['responseConfirm']) + int(res['requestConfirm']) == 2:
                # Add to confirmed trades once both confirmed
                ConfirmedTrade.add(pendingtradeid=tradeid, requestusername=res['requestUsername'],
                                   responseusername=res['requestUsername'], requestequipid=res['requestEquipID'],
                                   responseequipid=res['responseEquipID'])
                # Remove from pending trades
                PendingTrade.remove(pendingtradeid=tradeid)
                # Decrement count from respective users, delete if no more
                res2 = StudentHasEquipment.decrementQuantity(username=res['requestUsername'],
                                                             equipid=res['requestEquipID'])
                res2=res2[0]
                print("requesting quantity", res2)
                if res2['quantity'] == 0:
                    print("deleting requesting user's items")
                    StudentHasEquipment.remove(username=res['requestUsername'], equipid=res['requestEquipID'])

                res2 = StudentHasEquipment.decrementQuantity(username=res['responseUsername'],
                                                             equipid=res['responseEquipID'])

                res2 = res2[0]

                print("responding quantity", res2)
                if res2['quantity'] == 0:
                    print("deleting requesting user's items")
                    StudentHasEquipment.remove(username=res['responseUsername'], equipid=res['responseEquipID'])

        except IntegrityError:
            return HttpResponseRedirect('/student/' + username)

        return HttpResponseRedirect('/student/' + username)
    else:
        return HttpResponseRedirect('/')
