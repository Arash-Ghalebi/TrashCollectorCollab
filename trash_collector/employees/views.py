from django.apps import apps
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import date

from .models import Employee 
from .models import Customer
from .models import Account 

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Employee = apps.get_model('employees.Employee')
    logged_in_user = request.user 
    Customer = apps.get_model('customers.Customer')
    today = date.today
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        customer_zip = Customer.objects.filter(zip_code=logged_in_employee.zip_code) 
        daily_pickups = Customer.ojects.filter() 
        
        today = date.today()
        
        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'customer_zip' : customer_zip,
            'daily_pickups' : daily_pickups, 
            
        }

        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))
    # DICTIONARY:
        #return 
            # All pickup addresses in zip
            # Do not show suspended Accounts 
    
@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user, address=address_from_form, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')

@login_required
def edit_profile(request):
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        today = date.today()
        
        context = {
            'logged_in_employee': logged_in_employee,
            'today': today
        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))
    # return render(request, 'employees/index.html')    
# Employee = apps.get_model('employees.Employee')
# logged_in_user = request.user


# @login_required
# def edit_profile(request):
#     logged_in_user = request.user
#     logged_in_employee = Employee.objects.get(user=logged_in_user)
#     if request.method == "POST":
#         name_from_form = request.POST.get('name')
#         address_from_form = request.POST.get('address')
#         zip_from_form = request.POST.get('zip_code')
#         logged_in_employee.name = name_from_form
#         logged_in_employee.address = address_from_form
#         logged_in_employee.zip_code = zip_from_form
#         logged_in_employee.save()
#         return HttpResponseRedirect(reverse('employees:index'))
#     else:
#         context = {
#             'logged_in_employee': logged_in_employee
#         }
#         return render(request, 'employees/edit_profile.html', context)

# @login_required
# def create(request):
#     logged_in_user = request.user
#     if request.method == "POST":
#         name_from_form = request.POST.get('name')
#         address_from_form = request.POST.get('address')
#         zip_from_form = request.POST.get('zip_code')
#         new_employee = Employee(name=name_from_form, user=logged_in_user, address=address_from_form, zip_code=zip_from_form)
#         new_employee.save()
#         return HttpResponseRedirect(reverse('employee:index'))
#     else:
#         return render(request, 'employee/create.html')
    
# @login_required
# def my_pickups(request):
#     logged_in_employee = request.employee
#     logged_in_employee = Employee.objects.get(employee=logged_in_user)
#     if request.method == "POST":
#         date_from_form = request.POST.get('date')
        
#         # logged_in_customer.one_time_pickup = date_from_form
#         logged_in_employee.save()
#         return HttpResponseRedirect(reverse('customers:index'))
#     else:
#         context = {
#             'logged_in_employee': logged_in_employee
#         }
#         return render(request, 'employees/my_pickups.html', context)