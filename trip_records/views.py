from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.views.decorators.cache import cache_page
from django.views.generic import ListView

from .forms import DriverTripRecordForm, FuelPurchaseRecordForm, StopFormSet
from .gpt_utils import OpenAICompletionClient
from .models import DriverTripRecord, FuelPurchaseRecord, Stop


# Create your views here.


@cache_page(60 * 15)
def index(request):
    return render(request, 'index.html')


class DriverTripRecordListView(ListView):
    model = DriverTripRecord
    template_name = 'driver_trip_record_list.html'
    context_object_name = 'driver_trip_records'
    paginate_by = 10  # Number of records per page
    ordering = ['id']


def driver_trip_record(request):
    if request.method == 'POST':
        form = DriverTripRecordForm(request.POST)
        formset = StopFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            trip_record = form.save()
            formset.instance = trip_record
            formset.save()
            return redirect('driver_trip_record_list')
    else:
        form = DriverTripRecordForm()
        formset = StopFormSet()
    return render(request, 'driver_trip_record.html', {'form': form, 'formset': formset})


def edit_driver_trip_record(request, pk):
    record = get_object_or_404(DriverTripRecord, pk=pk)
    if request.method == 'POST':
        form = DriverTripRecordForm(request.POST, instance=record)

        formset = StopFormSet(request.POST, instance=record)
        # print(form.errors)
        print(formset.errors)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('driver_trip_record_list')
    else:
        form = DriverTripRecordForm(instance=record)
        formset = StopFormSet(instance=record)
    return render(request, 'driver_trip_record.html', {'form': form, 'formset': formset})


###############################################################################################################

class FuelPurchaseRecordListView(ListView):
    model = FuelPurchaseRecord
    template_name = 'fuel_purchase_record_list.html'
    context_object_name = 'fuel_purchase_records'
    paginate_by = 10  # Number of records per page
    ordering = ['id']


def fuel_purchase_record(request):
    if request.method == 'POST':
        form = FuelPurchaseRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fuel_purchase_record_list')
    else:
        form = FuelPurchaseRecordForm()
    return render(request, 'fuel_purchase_record.html', {'form': form})


def edit_fuel_purchase_record(request, pk):
    record = get_object_or_404(FuelPurchaseRecord, pk=pk)
    if request.method == 'POST':
        form = FuelPurchaseRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('fuel_purchase_record_list')
    else:
        form = FuelPurchaseRecordForm(instance=record)
    return render(request, 'fuel_purchase_record.html', {'form': form})


def get_unique_locations(request):
    query = request.GET.get('q', '')
    starting_locations = DriverTripRecord.objects.filter(starting_location__icontains=query).values_list('starting_location', flat=True).distinct()
    ending_locations = DriverTripRecord.objects.filter(ending_location__icontains=query).values_list('ending_location', flat=True).distinct()

    unique_locations = list(set(starting_locations) | set(ending_locations))
    return JsonResponse({'locations': unique_locations})




def report(request, trip_id):
    trip = DriverTripRecord.objects.get(pk=trip_id)
    fuel_purchases = FuelPurchaseRecord.objects.all()  # Adjust query as needed
    client = OpenAICompletionClient('gpt-3.5-turbo-0125')
    start_location = trip.starting_location
    ending_location = trip.ending_location

    journey_detail = trip.stops.all().values_list()

    response = client.send_request(data=journey_detail, start_location=start_location, ending_location=ending_location)

    return render(request, 'report.html', {'trip': trip, 'stops': response['journey'], 'fuel_purchases': fuel_purchases, })