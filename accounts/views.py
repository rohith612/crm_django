from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import inlineformset_factory

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter

from django.contrib import messages

from .models import *


# Create your views here.

@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.warning(request, 'Invalid username or password')
    context = {}
    return render(request, 'accounts/login.html', context)


@unauthenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        # print(request.POST)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login_page')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def logout_page(request):
    logout(request)
    return redirect('login_page')


@login_required(login_url='login_page')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['customer'])
def user_page(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['customer'])
def account_settings(request):
    customer_details = request.user.customer
    form = CustomerForm(instance=customer_details)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer_details)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def product(request):
    products = Product.objects.all()
    return render(request, 'accounts/product.html', {'products': products})
    # return HttpResponse('profile page')


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer_details = Customer.objects.get(id=pk)
    orders = customer_details.order_set.all()

    total_orders = orders.count()

    order_filter = OrderFilter(request.GET, queryset=orders)
    orders = order_filter.qs

    context = {'customer': customer_details, 'orders': orders,
               'total_orders': total_orders, 'order_filter': order_filter}
    return render(request, 'accounts/customer.html', context)
    # return HttpResponse('sample page')


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    order_form_set = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer_details = Customer.objects.get(id=pk)
    # form = OrderForm(initial={'customer': customer_details})
    form_set = order_form_set(queryset=Order.objects.none(), instance=customer_details)
    if request.method == 'POST':
        form_set = order_form_set(request.POST, instance=customer_details)
        # form = OrderForm(request.POST)
        if form_set.is_valid():
            form_set.save()
            return redirect('/')

    context = {'form': form_set}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
            # redirected to same page
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete_order.html', context)


@login_required(login_url='login_page')
def user_permissions(request):
    return HttpResponse('hello world')
