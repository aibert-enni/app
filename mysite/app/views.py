from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from .models import Numbers
from .models import Institutes


# Create your views here.
def ipphone(request):
    return render(request, 'ipphone.html')


def search_numbers(request):
    query = request.GET.get('q', '')
    if query:
        items = Numbers.objects.filter(name__istartswith=query)
    else:
        items = Numbers.objects.all()
    print("items: ", query)
    return render(request, 'admin/numbers_result_list.html', {'items': items})

def numbers(request):
    numbersData = list(Numbers.objects.values("id", "name", "institute__name", "position", "cabinet", "email", "local_number"))
    institutesData = list(Institutes.objects.values("id", "name"))
    return JsonResponse({"numbers": numbersData, "institutes": institutesData})

def admin(request):
    return
