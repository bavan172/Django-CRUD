#from mysite.myapp.decorators import unauthenticated_user
from django.db.models.aggregates import Count
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory  #used to create multiple form within a form
from django.contrib import messages  # for confirmation or error messages in login/registration forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # to restrict homepage before login
from django.contrib.auth.models import Group

from .decorators import *
from .filters import *
from .models import *
from .forms import *

# Create your views here.
@unauthenticated_user
def register(request):   
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST) # customized form
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username') # gets username from form 
                group = Group.objects.get(name='customer') # gets group from group table
                user.groups.add(group) # adds group to user

                messages.success(request,'Account was successfully created for ' + username)
                return redirect('login')

        context = {'form':form}
        return render(request,'myapp/register.html',context)

@unauthenticated_user
def loginPage(request):    
        if request.method == 'POST': 
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            # after authenticating we check if the user is present in the database
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Username OR Password is incorrect")  


        context = {}
        return render(request,'myapp/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
#@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders':orders,
        'customers':customers,
        'total_customers': total_customers,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
    }
    return render(request,"myapp/dashboard.html",context)

@login_required(login_url='login')
@allowed_users(allowed=['admin'])
def product(request):
    products = Product.objects.all()
    return render(request,"myapp/product.html",{'products':products})   

@login_required(login_url='login')
@allowed_users(allowed=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all() #order_set querying customer child object from the models
    order_count = orders.count()

    #code for filter
    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs

    context = {
        'customer':customer,
        'orders':orders,
        'order_count':order_count,
        'myFilter':myFilter,
    }

    return render(request,"myapp/customer.html",context)    

@login_required(login_url='login')
@allowed_users(allowed=['admin'])
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=10) # parent and child model,creating reference
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form = OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)

        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        'formset':formset,
    }
    return render(request,'myapp/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)  #  item instance we fill out in a form

    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')


    context = {'form':form}
    return render(request,'myapp/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item':order}    
    return render(request,'myapp/delete.html',context)

