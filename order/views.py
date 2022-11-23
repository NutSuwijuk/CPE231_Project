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

class OrdersList(View):
    def get(self, request):
        orders = list(OrderRecord.objects.order_by('order_no').all().values())
        data = dict()
        data['orders'] = orders

        return JsonResponse(data)

class OrdersDetail(View):
    def get(self, request, order_no):
        order = list(Users.objects.filter(order_no=order_no).values())
        data = dict()
        data['orders'] = order

        return JsonResponse(data)

class OrdersForm(forms.ModelForm):
    class Meta:
        model = OrderRecord
        fields = '__all__'

class OrderLineItemForm(forms.ModelForm):
    class Meta:
        model = OrderRecord
        fields = '__all__'

@method_decorator(csrf_exempt, name='dispatch')
class OrdersCreate(View):
    def post(self, request):
        data = dict()
        request.POST = request.POST.copy()
        if Orders.objects.count() != 0:
            order_no_max = Orders.objects.aggregate(Max('order_no'))['order_no__max']
            if (int(order_no_max[2:])+1) in range(1,10) :
                next_order_no = str(order_no_max[0:2]) + '000' + str(int(order_no_max[2:])+1)
            elif (int(order_no_max[2:])+1) in range(10,100) :
                next_order_no = str(order_no_max[0:2]) + '00' + str(int(order_no_max[2:])+1)
            elif (int(order_no_max[2:])+1) in range(100,1000) :
                next_order_no = str(order_no_max[0:2]) + '0' + str(int(order_no_max[2:])+1)  
            elif (int(order_no_max[2:])+1) in range(1000,10000) :
                next_order_no = str(order_no_max[0:2]) + '' + str(int(order_no_max[2:])+1)   
        else:
            next_order_no = "od0001"
        request.POST['order_no'] = next_order_no
        request.POST['id_user'] = request.POST['id_user']
        request.POST['date'] = reFormatDateMMDDYYYY(request.POST['date'])
        request.POST['total_price'] = reFormatNumber(request.POST['total_price'])
        request.POST['payment_method'] = request.POST['payment_method']
        request.POST['received'] = request.POST['received']
        request.POST['change'] = reFormatNumber(request.POST['change'])

        form = OrdersForm(request.POST)
        if form.is_valid():
            order = form.save()

            dict_lineitem = json.loads(request.POST['lineitem'])
            for lineitem in dict_lineitem['lineitem']:
                menu_id = Menu.objects.get(pk=lineitem['menu_id'])
                OrderLineItem.objects.create(
                    order_no=order,
                    menu_id=menu_id,
                    type=type,
                    sweet_level=reFormatNumber(lineitem['sweet_level']),
                    amount=reFormatNumber(lineitem['amount'])
                )

            data['order'] = model_to_dict(order)
        else:
            data['error'] = 'form not valid!'

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

@method_decorator(csrf_exempt, name='dispatch')
class OrdersUpdate(View):
    def post(self, request, pk):
        order_no = pk 
        data = dict()
        order = Orders.objects.get(pk=order_no)
        request.POST = request.POST.copy()
        request.POST['order_no'] = order_no
        request.POST['id_user'] = request.POST['id_user']
        request.POST['date'] = reFormatDateMMDDYYYY(request.POST['date'])
        request.POST['total_price'] = reFormatNumber(request.POST['total_price'])
        request.POST['payment_method'] = request.POST['payment_method']
        request.POST['received'] = reFormatNumber(request.POST['received'])
        request.POST['change'] = reFormatNumber(request.POST['change'])

        form = OrderForm(instance=order, data=request.POST)
        if form.is_valid():
            order = form.save()

            OrderLineItem.objects.filter(order_no=order_no).delete()

            dict_lineitem = json.loads(request.POST['lineitem'])
            for lineitem in dict_lineitem['lineitem']:
                menu_id = Menu.objects.get(pk=lineitem['menu_id'])
                OrderLineItem.objects.create(
                    order_no=order,
                    menu_id=menu_id,
                    type=type,
                    sweet_level=reFormatNumber(lineitem['sweet_level']),
                    amount=reFormatNumber(lineitem['amount'])
                )

            data['order'] = model_to_dict(order)
        else:
            data['error'] = 'form not valid!'

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

@method_decorator(csrf_exempt, name='dispatch')
class OrdersDelete(View):
    def post(self, request, pk):
        order_no = pk
        data = dict()
        orders = Orders.objects.get(pk=order_no)
        if orders:
            orders.delete()
            data['message'] = "Order Deleted!"
        else:
            data['message'] = "Error!"

        return JsonResponse(data)

# class OrderPDF(View):
#     def get(self, request, pk):
#         order_no = pk

#         order = list(Order.objects.select_related("customer_id").filter(order_no=order_no).values('order_no', 'customer_id', 'date', 'total','promotion_code','payment_method','employee_id','rebate','remain'))
#         orderlineitem = list(OrderLineItem.objects.select_related('menu_code').filter(order_no=order_no).order_by('item_no').values("item_no","order_no","menu_code","unit_price","quantity","product_total"))
#         #invoicelineitem = InvoiceLineItem.objects.raw(
#         #    "SELECT * "
#         #    "FROM invoice_line_item LIT "
#         #    "  JOIN product P ON LIT.product_code = P.code "
#         #    "WHERE LIT.invoice_no = '{}'" .format(invoice_no)
#         #)

#         #list_lineitem = [] 
#         #for lineitem in invoicelineitem:
#         #    dict_lineitem = json.loads(str(lineitem))
#         #    dict_lineitem['product_name'] = lineitem.product_code.name
#         #    dict_lineitem['units'] = lineitem.product_code.units
#         #    list_lineitem.append(dict_lineitem)

#         data = dict()
#         data['order'] = order[0]
#         data['orderlineitem'] = orderlineitem
        
#         #return JsonResponse(data)
#         return render(request, 'order/pdf.html', data)

class OrdersReport(View):
    def get(self, request):

        with connection.cursor() as cursor:
            cursor.execute('SELECT o.order_no as "Order No", o.date as "Date" '
                           ' , m.menu_id as "Menu ID", o.id_user as "Customer ID", oli.type as "Type"'
                           ' , oli.sweet_level as "Level", oli.amount as "Amount", m.price as "Price" '
                           ' , o.total_price as "Total Price", o.payment_method as "Payment Method" '
                           ' , o.received as "Received", o.change as "Change" '
                           ' FROM orders o JOIN order_line_item oli ON o.order_no = oli.order_no '
                           ' JOIN menu m ON m.menu_id = oli.menu_id'
                           ' ORDER BY o.order_no')
            
            row = dictfetchall(cursor)
            column_name = [col[0] for col in cursor.description]

        data = dict()
        data['column_name'] = column_name
        data['data'] = row
        
        #return JsonResponse(data)
        return render(request, 'order/report.html', data)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [name[0].replace(" ", "_").lower() for name in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def reFormatDateMMDDYYYY(ddmmyyyy):
        if (ddmmyyyy == ''):
            return ''
        return ddmmyyyy[3:5] + "/" + ddmmyyyy[:2] + "/" + ddmmyyyy[6:]

def reFormatNumber(str):
        if (str == ''):
            return ''
        return str.replace(",", "")