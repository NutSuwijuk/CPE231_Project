from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.db.models import Max
from django.db import transaction
from .models import *
import json
import re

# Create your views here.
def index(request):
    data = {}
    return render(request, 'general/index.html', data)

class StockList(View):
    def get(self, request):
        stocks = list(Stock.objects.all().values())
        data = dict()
        data['stocks'] = stocks

        return JsonResponse(data)

class IngredientList(View):
    def get(self, request):
        ingredients = list(Ingredient.objects.all().values)
        data = dict()
        data['ingredients'] = ingredients

        return JsonResponse(data)

class MenuList(View):
    def get(self, request):
        menus = list(Menu.objects.all().values())
        data = dict()
        data['menus'] = menus

        return JsonResponse(data)

class AdditionalItemsList(View):
    def get(self, request):
        additionalitems = list(AdditionalItems.objects.all().values())
        data = dict()
        data['additionalitems'] = additionalitems

        return JsonResponse(data)

class SweetList(View):
    def get(self, request):
        sweets = list(Sweet.objects.all().values())
        data = dict()
        data['sweets'] = sweets

        return JsonResponse(data)

class PaymentMethodList(View):
    def get(self, request):
        payment_methods = list(PaymentMethod.objects.all().values())
        data = dict()
        data['payment_methods'] = payment_methods

        return JsonResponse(data)

class PaymentMethodDetail(View):
    def get(self, request, payment_method):
        paymentmethod = list(PaymentMethod.objects.filter(payment_method=payment_method).values())
        data = dict()
        data['payment_methods'] = paymentmethod

        return JsonResponse(data)

class UsersList(View):
    def get(self, request):
        users = list(Users.objects.all().values())
        data = dict()
        data['users'] = users

        return JsonResponse(data)

class UsersDetail(View):
    def get(self, request, id_user):
        user = list(Users.objects.filter(id_user=id_user).values())
        data = dict()
        data['users'] = user

        return JsonResponse(data)

class OrderRecordList(View):
    def get(self, request):
        orders = list(OrderRecord.objects.order_by('order_no').all().values())
        data = dict()
        data['orders'] = orders

        return JsonResponse(data)

class OrderRecordDetail(View):
    def get(self, request, order_no):
        order = list(Users.objects.filter(order_no=order_no).values())
        data = dict()
        data['orders'] = order

        return JsonResponse(data)

class OrderRecordForm(forms.ModelForm):
    class Meta:
        model = OrderRecord
        fields = '__all__'

class OrderRecordLineItemForm(forms.ModelForm):
    class Meta:
        model = OrderRecord
        fields = '__all__'