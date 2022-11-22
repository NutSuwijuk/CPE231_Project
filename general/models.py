from django.db import models

# Create your models here.
class Stock(models.Model):
    id_stock = models.CharField(max_length=10,primary_key=True)
    date_stock = models.DateField(null=True)
    stock_name = models.CharField(max_length=100)
    amount = models.IntegerField(null=True)
    cost = models.FloatField(null=True, blank=True)
    total_amount = models.IntegerField(null=True)
    total_price = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = "stock"
        managed = False
    def __str__(self):
        return self.id_stock

# class Ingredient(models.Model):
#     code = models.CharField(max_length=10,primary_key=True)
#     name = models.CharField(max_length=100)
#     units = models.CharField(max_length=10)
#     product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, db_column='product_type')
#     class Meta:
#         db_table = "product"
#         managed = False
#     def __str__(self):
#         return self.code

class Menu(models.Model):
    menu_id = models.CharField(max_length=10, primary_key=True)
    menu_name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True, blank=True)
    amount_of_coffee = models.IntegerField(null=True)
    amount_of_milk = models.IntegerField(null=True)
    amount_of_chocolate = models.IntegerField(null=True)
    amount_of_syrub = models.IntegerField(null=True)
    class Meta:
        db_table = "menu"
        managed = False
    def __str__(self):
        return self.menu_id

class AdditionalItems(models.Model):
    type = models.CharField(max_length=10, primary_key=True)
    description = models.CharField(max_length=100, null=True)
    mash = models.IntegerField(null=True)
    class Meta:
        db_table = "additional_items"
        managed = False
    def __str__(self):
        return self.type

class Sweet(models.Model):
    sweet_level = models.CharField(max_length=10, primary_key=True)
    description = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = "sweet"
        managed = False
    def __str__(self):
        return self.sweet_level

class PaymentMethod(models.Model):
    payment_method = models.CharField(max_length=10,primary_key=True)
    description = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = "payment_method"
        managed = False
    def __str__(self):
        return self.payment_method

class Users(models.Model):
    id_user = models.CharField(max_length=10,primary_key=True)
    username = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone_number = models.IntegerField(null=True)
    password = models.CharField(max_length=10)
    point = models.IntegerField(null=True)
    class Meta:
        db_table = "users"
        managed = False
    def __str__(self):
        return self.id_user