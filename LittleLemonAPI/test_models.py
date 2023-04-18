from django.test import TestCase
from .models import  Booking
# Create your tests here.
#TestCase class
class MenuItemTest(TestCase):
    def test_get_item(self):
        item = MenuItem.objects.create(title="IceCream", price=80, category=1)
        self.assertEqual(item, "IceCream")