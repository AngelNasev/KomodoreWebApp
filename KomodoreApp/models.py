from django.contrib.auth.models import User
from django.db import models


# Create your models here.
def get_admin_user():
    return User.objects.get(username='admin')


class Car(models.Model):
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.manufacturer} {self.model} {self.year}"


class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images', null=True, blank=True)
    warranty = models.CharField(max_length=100,
                                choices=[("No Warranty", "No Warranty"), ("1 Year Warranty", "1 Year Warranty"),
                                         ("2 Year Warranty", "2 Year Warranty"),
                                         ("Lifetime Warranty", "Lifetime Warranty")])
    characteristics = models.TextField()
    description = models.TextField()
    cars = models.ManyToManyField(Car, related_name='products')
    category = models.CharField(max_length=100, choices=[("Batteries", "Batteries"), ("Engine Oil", "Engine Oil"),
                                                         ("Antifreeze", "Antifreeze"), ("Fuel Lines", "Fuel Lines"),
                                                         ("Exhaust", "Exhaust"),
                                                         ("Windshield Wipers", "Windshield Wipers"),
                                                         ("Brakes", "Brakes"), ("Engine Parts", "Engine Parts"),
                                                         ("Tires", "Tires"), ("Wheel Mountings", "Wheel Mountings")])

    def __str__(self):
        return f"{self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField('CartItem')

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def total(self):
        return float(self.product.price * int(self.quantity))