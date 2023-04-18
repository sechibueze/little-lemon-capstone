from django.db import models
from django.contrib.auth.models import Group , User

# Create your models here.
class Category(models.Model):
    # slug = models.SlugField()
    title = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.title
    
class Menu(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    featured = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.title
    
# Create your models here.
class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    reservation_date = models.DateField()
    reservation_slot = models.SmallIntegerField(default=10)

    def __str__(self): 
        return self.first_name

class Order(models.Model):
    label = models.CharField(max_length=255)
    delivered = models.BooleanField(default=False)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    crew = models.ForeignKey(Group,  on_delete=models.PROTECT)
    def __str__(self) -> str:
        return self.label

