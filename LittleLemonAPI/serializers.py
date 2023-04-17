from rest_framework import serializers
from .models import Menu, Category, Order
from django.contrib.auth.models import Group, User


# class LemonGroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LemonGroup
#         fields = '__all__'
# class LemonUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LemonUser
#         fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    class Meta:
        model = Menu
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    crew = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    menu = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all())
    # crew = serializers.StringRelatedField()
    # user = serializers.StringRelatedField()
    class Meta:
        model = Order
        fields = '__all__'
        depth = 1
