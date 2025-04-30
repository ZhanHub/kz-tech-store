# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from decimal import Decimal


# Басты бет (қазір жай жазамыз)
def home(request):
    return render(request, 'home.html')

# Тіркелу (Register)
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Тіркелу сәтті аяқталды! Енді кіріңіз.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Кіру (Login)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Шығу (Logout)
def logout_view(request):
    logout(request)
    return redirect('login')

#Product
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

from django.contrib.auth.decorators import login_required
from .models import Order, Customer

#Заказ жасау
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, Customer
from django.contrib.auth.decorators import login_required

@login_required
def make_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        if product.stock < quantity:
            return render(request, 'out_of_stock.html', {'product': product})

        total_price = quantity * product.price
        customer, created = Customer.objects.get_or_create(user=request.user)

        Order.objects.create(
            customer=customer,
            product=product,
            quantity=quantity,
            total_price=total_price
        )

        product.stock -= quantity
        product.save()

        return redirect('order_list')

    return redirect('product_list')


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user != order.customer.user:
        return redirect('order_list')

    product = order.product
    product.stock += order.quantity
    product.save()

    order.delete()

    return redirect('order_list')






from decimal import Decimal
from django.contrib import messages

@login_required
def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock == 0:
        return render(request, 'out_of_stock.html', {'product': product})

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_type = request.POST.get('payment_type')
        installment_months = int(request.POST.get('installment_months', 0))

        total_price = product.price
        monthly_payment = 0

        if payment_type == 'installment':
            monthly_payment = total_price / installment_months
        elif payment_type == 'credit':
            total_price = total_price * Decimal('1.05')
            monthly_payment = total_price / installment_months

        customer, created = Customer.objects.get_or_create(user=request.user)

        # Тапсырысты базаға сақтау
        Order.objects.create(
            customer=customer,
            product=product,
            quantity=1,
            total_price=total_price,
            name=name,
            phone=phone,
            address=address,
            payment_type=payment_type,
            months=installment_months if payment_type != 'full' else None
        )

        # Стоктан 1-ге азайту
        product.stock -= 1
        product.save()

        # 🔥 Сессияға сақтау
        request.session['payment_type'] = payment_type
        request.session['monthly_payment'] = float(monthly_payment)
        request.session['installment_months'] = installment_months
        request.session['total_price'] = float(total_price)

        return redirect('payment_success')

    return render(request, 'checkout.html', {'product': product})


@login_required
def payment_success(request):
    context = {
        'payment_type': request.session.get('payment_type'),
        'monthly_payment': request.session.get('monthly_payment'),
        'installment_months': request.session.get('installment_months'),
        'total_price': request.session.get('total_price'),
    }
    return render(request, 'payment_success.html', context)





from django.db import connection

def log_user_action(username, action, path):
    with connection.cursor() as cursor:
        cursor.execute("SELECT log_user_action(%s, %s, %s)", [username, action, path])

from django.contrib.auth.decorators import login_required

@login_required
def some_page_view(request):
    log_user_action(request.user.username, "бетке кірді", request.path)
    return render(request, 'some_template.html')

# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserActivityLog

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def monitoring_view(request):
    logs = UserActivityLog.objects.all().order_by('-created_at')  # Соңғы әрекеттер жоғарыда
    return render(request, 'monitoring.html', {'logs': logs})









from .models import Category, Brand, Order

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'brand_list.html', {'brands': brands})

@login_required
def order_list(request):
    customer = get_object_or_404(Customer, user=request.user)
    orders = Order.objects.filter(customer=customer)

    return render(request, 'order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    customer = get_object_or_404(Customer, user=request.user)
    order = get_object_or_404(Order, id=order_id, customer=customer)

    # Ай сайынғы төлем есептеу
    monthly_payment = None
    if order.payment_type in ['installment', 'credit'] and order.months:
        monthly_payment = order.total_price / order.months

    return render(request, 'order_detail.html', {
        'order': order,
        'monthly_payment': monthly_payment,
    })

