from django.db import models
from django.contrib.auth.models import User

# Категория моделі
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Бренд моделі
class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

# Өнім (Product) моделі
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

# Сатып алушы (Customer) моделі — МІНДЕТТІ түрде керек!
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

# Тапсырыс (Order) моделі
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    name = models.CharField(max_length=100, default='Аты жоқ')
    phone = models.CharField(max_length=20, default='0000000000')
    address = models.TextField(default='Адрес жоқ')
    payment_type = models.CharField(max_length=20, default='full')  # full / installment / credit
    months = models.PositiveIntegerField(null=True, blank=True)  # optional

    order_date = models.DateTimeField(auto_now_add=True)  # Атты өзгертпедім

    def __str__(self):
        return f"{self.product.name} - {self.customer.user.username}"
    
# models.py
# app_main/models.py (сенің проектте қайда болса сонда жазамыз)

from django.db import models

class UserActivityLog(models.Model):
    username = models.CharField(max_length=150)
    action = models.TextField()
    path = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'user_activity_log'  # Нақты кесте аты
        managed = False  # Django оны басқара алмайды (Migration жасамаймыз)

    def __str__(self):
        return f"{self.username} - {self.created_at}"



