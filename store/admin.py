from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Brand, Product, Customer, Order

# Модельдерді тіркеу
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)

# app_main/admin.py
from .models import UserActivityLog

@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('username', 'action', 'path', 'created_at')
    ordering = ('-created_at',)
