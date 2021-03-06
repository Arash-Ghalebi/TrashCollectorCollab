from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name="create"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    # path('one_time/', views.my_pickups, name="my_pickups"),
    path('add_charge/<int:customer_id>/', views.add_charge, name = "add_charge"),
    path('weekly_pickup/', views.weekly_pickup, name="weekly_pickup"),   
    
]