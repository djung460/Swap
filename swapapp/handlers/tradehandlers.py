from sqlite3 import IntegrityError
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from swapapp.models import Student, ConfirmedTrade, PendingTrade, StudentHasEquipment


@csrf_exempt
def addpending(request):
    """
    Moved to handler.py
    """
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
                                   responseusername=res['responseUsername'], requestequipid=res['requestEquipID'],
                                   responseequipid=res['responseEquipID'])
                # Remove from pending trades
                PendingTrade.remove(pendingtradeid=tradeid)

                # Decrement quantity from students, delete if no more
                quant = StudentHasEquipment.decrementQuantity(username=res['requestUsername'],
                                                             equipid=res['requestEquipID'])
                quant=quant[0]
                print("requesting quantity", quant)

                if quant['quantity'] == 0:
                    print("deleting requesting user's items")
                    StudentHasEquipment.remove(username=res['requestUsername'], equipid=res['requestEquipID'])

                quant = StudentHasEquipment.decrementQuantity(username=res['responseUsername'],
                                                             equipid=res['responseEquipID'])
                quant = quant[0]

                print("responding quantity", quant)
                if quant['quantity'] == 0:
                    print("deleting requesting user's items")
                    StudentHasEquipment.remove(username=res['responseUsername'], equipid=res['responseEquipID'])

                # Increment quantity of traded item from students, add if it doesn't exist
                StudentHasEquipment.addOrIncrement(username=res['requestUsername'], equipid=res['responseEquipID'])
                StudentHasEquipment.addOrIncrement(username=res['responseUsername'], equipid=res['requestEquipID'])

        except IntegrityError:
            return HttpResponseRedirect('/student/' + username)

        return HttpResponseRedirect('/student/' + username)
    else:
        return HttpResponseRedirect('/')
