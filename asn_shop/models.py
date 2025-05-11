from django.db import models
from django.contrib.auth.models import AbstractUser


# Модель пользователя (кастомный пользователь)
class MyUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username


# Модель категории автомобилей
class CarCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


# Модель производителя
class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    founded_year = models.IntegerField()

    def __str__(self):
        return self.name


# Модель автомобиля
class Car(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='car_images/', null=True, blank=True)
    
    # Связь с пользователем
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    
    # Связь с категорией
    category = models.ForeignKey(CarCategory, on_delete=models.CASCADE)
    
    # Связь с производителем
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.year})"


# Модель заказа
class Order(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    buyer = models.ForeignKey(MyUser, related_name='buyer_orders', on_delete=models.CASCADE)
    seller = models.ForeignKey(MyUser, related_name='seller_orders', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена автомобиля в заказе
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"Order #{self.id} for {self.car.name} from {self.seller.username} to {self.buyer.username}"


# Модель отзывов о машинах
class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    rating = models.IntegerField()  # Рейтинг от 1 до 5
    comment = models.TextField()

    def __str__(self):
        return f"Review for {self.car.name} by {self.user.username}"
