import datetime
from django.db import models
from django.utils.timezone import now




# Car Make model
class CarMake(models.Model):
   name = models.CharField(null=False, max_length=50)
   description = models.CharField(null=True, max_length=500)


   def __str__(self):
       return self.name


# Car Model model

class CarModel(models.Model):
   car_make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
   name = models.CharField(null=False, max_length=50)
   dealer_id = models.IntegerField(null=True)


   SEDAN = "Sedan"
   SUV = "SUV"
   WAGON = "Wagon"
   SPORT = "Sport"
   COUPE = "Coupe"
   MINIVAN = "Mini"
   VAN = "Van"
   PICKUP = "Pickup"
   TRUCK = "Truck"
   BIKE = "Bike"
   SCOOTER = "Scooter"
   OTHER = "Other"
   CAR_CHOICES = [(SEDAN, "Sedan"), (SUV, "SUV"), (WAGON, "Station wagon"), (SPORT, "Sports Car"),
                  (COUPE, "Coupe"), (MINIVAN, "Mini van"), (VAN,
                                                            "Van"), (PICKUP, "Pick-up truck"),
                  (TRUCK, "Truck"), (BIKE, "Motor bike"), (SCOOTER, "Scooter"), (OTHER, 'Other')]
   model_type = models.CharField(
       null=False, max_length=15, choices=CAR_CHOICES, default=SEDAN)


   YEAR_CHOICES = []
   for r in range(1969, (datetime.datetime.now().year+1)):
       YEAR_CHOICES.append((r, r))


   year = models.IntegerField(
       ('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)


   def __str__(self):
       return self.name + ", " + str(self.year) + ", " + self.model_type




class CarDealer:
   def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
       # Dealer address
       self.address = address
       # Dealer city
       self.city = city
       # Dealer Full Name
       self.full_name = full_name
       # Dealer id
       self.id = id
       # Location lat
       self.lat = lat
       # Location long
       self.long = long
       # Dealer short name
       self.short_name = short_name
       # Dealer state
       self.st = st
       # Dealer zip
       self.zip = zip
   def __str__(self):
       return "Dealer name: " + self.full_name


class DealerReview:
   def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
       self.dealership = dealership
       self.name = name
       self.purchase = purchase
       self.review = review
       self.purchase_date = purchase_date
       self.car_make = car_make
       self.car_model = car_model
       self.car_year = car_year
       self.sentiment = sentiment
       self.id = id
