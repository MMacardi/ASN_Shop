from django.contrib import admin
from .models import MyUser, Car, CarCategory, Order, Review, Manufacturer, CarImage

admin.site.register(MyUser)
admin.site.register(Car)
admin.site.register(CarCategory)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Manufacturer)
