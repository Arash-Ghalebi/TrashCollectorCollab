from django.apps import apps
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import date
import datetime
import calendar


from .models import Employee 
# from .models import Customer

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Employee = apps.get_model('employees.Employee')
    logged_in_user = request.user 
    Customer = apps.get_model('customers.Customer')
    week_days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    today = date.today()
    week_num = datetime.date.today().weekday()
    week_string = week_days[week_num]
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        customer_zip = Customer.objects.filter(zip_code=logged_in_employee.zip_code) 
        daily_pickups = customer_zip.filter(weekly_pickup=week_string) | customer_zip.filter(one_time_pickup=today)
        not_suspended = daily_pickups.exclude(suspend_start__lte=today, suspend_end__gte=today) #| daily_pickups.exclude(suspend_start=NULL)
        final_list = not_suspended.exclude(date_of_last_pickup=today)
        
        today = date.today()
        
        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'final_list' : final_list,
            
        }

        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))
    
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

def add_charge(request, customer_id):
    Customer = apps.get_model('customers.Customer')
    customer = Customer.objects.get(id=customer_id)
    customer.balance += 20
    customer.date_of_last_pickup = date.today()
    customer.save()
    print("successful pickup")
    return HttpResponseRedirect(reverse('employees:index'))

def pick_day(request, customer_id):
    Customer = apps.get_model('customers.Customer')
    customer = Customer.objects.get(id=customer_id)
    

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)

def weekly_pickup(request):
    Customer = apps.get_model('customers.Customer')
    day_of_week = request.POST.get("weekly_pickup")
    customers = Customer.objects.filter(weekly_pickup=day_of_week)
    context = {
        'final_list': customers,
    }
    return render(request, 'employees/select_day.html', context)