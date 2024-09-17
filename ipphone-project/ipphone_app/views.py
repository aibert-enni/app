from django.http import JsonResponse
from django.views.generic import TemplateView

from .models import Numbers
from .models import Institutes


# Create your views here.

class Ipphone(TemplateView):
    template_name = "ipphone.html"

def numbers(request):
    numbersData = list(Numbers.objects.values("id", "name", "institute__name", "position", "cabinet", "email", "local_number"))
    institutesData = list(Institutes.objects.values("id", "name"))
    return JsonResponse({"numbers": numbersData, "institutes": institutesData})