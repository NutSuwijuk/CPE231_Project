from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import connection

from report.models import *
import json

# Create your views here.
<<<<<<< HEAD
# def index(request):
#     # return render(request, '/Home/index.html')
#     return JsonResponse(request)
def Home(request):
    return render(request, '/Home/index.html')
=======
def index(request):
    return render(request, 'base.html')
>>>>>>> e8c65b91597053e807a6089239eec7be3e49a216

def Home(request):
    return render(request, 'Home/Home.html')

def recommended_menu(request):
    return render(request, 'Home/Recommended_Menu.html')

def promotion(request):
    return render(request, 'Home/Promotion.html')