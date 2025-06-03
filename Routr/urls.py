"""
URL configuration for Routr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from trip_records.views import index, fuel_purchase_record, driver_trip_record, DriverTripRecordListView, FuelPurchaseRecordListView, edit_driver_trip_record, \
    edit_fuel_purchase_record, get_unique_locations, report

urlpatterns = [
    path('', index),
    path('driver_trip_form/', driver_trip_record, name='driver_trip_record'),
    path('fuel_purchase_form/', fuel_purchase_record, name='fuel_purchase_record'),
    path('driver_trip_list/', DriverTripRecordListView.as_view(), name='driver_trip_record_list'),
    path('fuel_purchase_list/', FuelPurchaseRecordListView.as_view(), name='fuel_purchase_record_list'),
    path('driver_trip/edit/<int:pk>/', edit_driver_trip_record, name='edit_driver_trip_record'),
    path('fuel_purchase/edit/<int:pk>/', edit_fuel_purchase_record, name='edit_fuel_purchase_record'),
    path('get_unique_locations/', get_unique_locations, name='get_unique_locations'),
    path('report/<int:trip_id>/', report, name='report'),

    path('admin/', admin.site.urls),
]