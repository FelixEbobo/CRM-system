from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import product, order, customer
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='LoginPage')
def home(request):
    orders = order.objects.all()
    customers = customer.objects.all()

    num_customers = customers.count()
    num_orders = orders.count()

    orders_pend = orders.filter(status='Pending').count()
    last_orders = orders.order_by('-date_created')[:5]

    context = {'orders': orders, "customers": customers, 
               'num_customers': num_customers, 'num_orders': num_orders,
               'orders_pend': orders_pend, 'last_orders': last_orders,
               'orders_del': num_orders - orders_pend,}

    return render(request, 'accounts/dashboard.html', context=context)

@unauthenticated_user
def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groupts.add(Group.objects.get('customer'))

            return redirect('LoginPage')

    context = {'form': form}
    return render(request, 'accounts/register.html', context=context)

@unauthenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Home')
    context = {}
    return render(request, 'accounts/login.html', context=context)

def logout_user(request):
    logout(request)
    return redirect('LoginPage')

def user_page(request):
    context = {}
    return render(request, 'accounts/user.html', context=context)

def products(request):
    products = product.objects.all()
    return render(request, 'accounts/products.html',
        {'products': products})

@login_required(login_url='LoginPage')
@allowed_users(allowed_roles=('admin',))
def customer1(request, pk):
    customer_ = customer.objects.get(id=pk)
    orders = customer_.order_set.all()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer_, 'orders': orders,
               'products': products, 'filter': myFilter,}
    return render(request, 'accounts/customer.html', context=context)
    
@login_required(login_url='LoginPage')
def create_order(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context=context)

@login_required(login_url='LoginPage')
def update_order(request, pk):

    order_ = order.objects.get(id=pk)
    form = OrderForm(instance=order_)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order_)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context=context)

@login_required(login_url='LoginPage')
def delete_order(request, pk):
    item = order.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect('/')
        
    context = {'item': item}
    return render(request, 'accounts/delete.html', context=context)