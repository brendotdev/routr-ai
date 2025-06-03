from django.db import models


class DriverTripRecord(models.Model):
    date = models.DateField()
    company_name = models.CharField(max_length=255)
    driver_name = models.CharField(max_length=255)
    manifest = models.CharField(max_length=255, blank=True, null=True)
    truck_no = models.CharField(max_length=255, blank=True, null=True)
    trailer_no = models.CharField(max_length=255, blank=True, null=True)

    start_time = models.TimeField()
    end_time = models.TimeField()
    starting_mileage = models.DecimalField(max_digits=10, decimal_places=2)
    ending_mileage = models.DecimalField(max_digits=10, decimal_places=2)
    starting_location = models.CharField(max_length=255)
    ending_location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.date} - {self.driver_name} - {self.company_name} - Start: {self.starting_location} - End: {self.ending_location}"


class Stop(models.Model):
    trip_record = models.ForeignKey(DriverTripRecord, on_delete=models.CASCADE, related_name='stops')
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_address = models.CharField(max_length=255, blank=True, null=True)
    pallets_in = models.IntegerField(blank=True, null=True)
    pallets_out = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Stop for {self.trip_record} - {self.customer_name}"


class FuelPurchaseRecord(models.Model):

    state = models.CharField(max_length=100)
    date = models.DateField()
    invoice_number = models.CharField(max_length=100)
    gallons = models.DecimalField(max_digits=10, decimal_places=2)
    dollar_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_stop_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    trip_record = models.OneToOneField(DriverTripRecord, on_delete=models.CASCADE, related_name='fuel_purchase', null=True, blank=True)


    def __str__(self):
        return f"{self.date} - {self.invoice_number}"