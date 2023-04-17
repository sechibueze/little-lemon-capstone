from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage
# Create your views here.
from .models import Menu, Order, Category
from .serializers import CategorySerializer, MenuSerializer, OrderSerializer

# 1. The admin can assign users to the manager group
# 2. You can access the manager group with an admin token
@api_view()
@permission_classes([IsAdminUser])
def manager(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        manager = Group.objects.get(name='Manager')
        if request.method == 'POST':
            manager.user_set.add(user)
        if request.method == 'DELETE':
            manager.user_set.remove(user)
        
        return Response({"status": True, "message": "User group updated"})
    
    return Response({"status": True,"message": 'Failed request'}, 403)

# 3. The admin can add menu items 
class MenuList(generics.ListCreateAPIView):
    permission_classes = []
    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'POST':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


# 4. The admin can add categories
class CategoryList(generics.ListCreateAPIView):
    permission_classes = []
    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'POST':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
# 5.Managers can log in => see login endpoint
# 6.Managers can update the item of the day

# 7.Managers can assign users to the delivery crew
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def assign_user_to_group(request):
    if not request.user.groups.filter(name='Manager').exists():
        return Response({"status": False, "nessage": 'Access denied'}, 403)
    
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        deliver_crew_group = Group.objects.get(name='DeliveryCrew')
        if request.method == 'PUT':
            deliver_crew_group.user_set.add(user)
        if request.method == 'DELETE':
            deliver_crew_group.user_set.remove(user)
        
        return Response({"status": True, "message": "User group updated"})
    
    return Response({"status": True,"message": 'Failed request'}, 403)

# 8.Managers can assign orders to the delivery crew
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def assign_orders_to_delivery(request, pk):
    if not request.user.groups.filter(name='Manager').exists():
        return Response({"status": False, "nessage": 'Access denied'}, 403)
    
    if not Group.objects.filter(name='DeliveryCrew').exists():
        return Response({"status": False, "nessage": 'DeliveryCrew not found'}, 403)
    
    delivery_crew_group = Group.objects.get(name='DeliveryCrew')
    order = Order.objects.get(pk=pk)
    if not order:
        return Response({"status": False, "nessage": 'Order not found'}, 400)
    
    data={"crew": delivery_crew_group.id}
    _order_serializer = OrderSerializer(instance=order, data=data, partial=True)
    if _order_serializer.is_valid():
        _order_serializer.save()
        return Response({"status": True, "data": _order_serializer.data,"message": 'Order Updated'}, 200)

 
    return Response({"status": _order_serializer.errors,"message": 'Failed request'}, 200)



# 9.The delivery crew can access orders assigned to them
@api_view()
@permission_classes([IsAuthenticated])
def get_orders_by_group(request):
    
    if request.user.is_authenticated:

        username = request.user.username
        user = User.objects.get(username=username)
        orders = Order.objects.all()
        if user.groups.filter(name="DeliveryCrew").exists():
            user_group = user.groups.get(name='DeliveryCrew')
            orders = Order.objects.filter(crew=user_group.id)
        result = OrderSerializer(orders, many=True)
        return Response({"data": result.data ,"status": True,"message": 'Success'}, 200)

    
    
    return Response({"status": True,"message": 'Failed request'}, 403)


# 10.The delivery crew can update an order as delivered
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_orders_status(request, pk):
    if not request.user.groups.filter(name='DeliveryCrew').exists():
        return Response({"status": False, "nessage": 'Access denied'}, 403)
    
    order = Order.objects.get(pk=pk)
    if not order:
        return Response({"status": False, "nessage": 'Order not found'}, 400)
    
    data={"delivered": True}
    _order_serializer = OrderSerializer(instance=order, data=data, partial=True)
    if _order_serializer.is_valid():
        _order_serializer.save()
        return Response({"status": True, "data": _order_serializer.data,"message": 'Order Updated'}, 200)

    return Response({"status": _order_serializer.errors,"message": 'Failed request'}, 200)



# 13. Customers can browse all categories 
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

# 14.Customers can browse all the menu items at once
# 15.Customers can browse menu items by category
# 16.	Customers can paginate menu items
# 17.	Customers can sort menu items by price
class MenuList(APIView):

    def get(self, request):
        menu_list = Menu.objects.all()
        category_filter = request.GET.get('category')
        ordering = request.GET.get('ordering')
        search = request.GET.get('search')
        page = request.query_params.get('page', default=1)
        per_page = request.query_params.get('per_page', default=3)

        if category_filter:
            menu_list = menu_list.filter(category__title=category_filter)
        if ordering:
            ordering_fields = ordering.split(",")
            menu_list = menu_list.order_by(*ordering_fields)
        if search:
            menu_list = menu_list.filter(title__icontains=search)
        
        paginator = Paginator(menu_list, per_page=per_page)
        try:
            menu_list = paginator.page(number=page)
        except EmptyPage:
            menu_list = []
        serializer = MenuSerializer(menu_list, many=True)
        return  Response({"data": serializer.data ,"status": True, "message": 'Welcome manager'})

class MenuItem(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        # menu_list = Menu.objects.select_related('category').all()
        menu = get_object_or_404(Menu,pk=pk)

        order = {
            "label": request.PUT.get('label', 'Little Lemmon'),
            "user": request.user,
            "menu": menu.id,
        }
        serializer = OrderSerializer(data=order)
        if serializer.is_valid():
            serializer.save()
            return  Response({ "data": serializer.data ,"status": True, "message": 'Order saved'})
        return  Response({ "data": serializer.errors ,"status": True, "message": 'Welcome manager'})

# 18.	Customers can add menu items to the cart
# 20.	Customers can place orders
# 19.	Customers can access previously added items in the cart
# 21.	Customers can browse their own orders
class OrderList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.select_related("crew", "menu", "user").all()
        if request.user.groups.filter(name="DeliveryCrew").exists():
            orders = orders.filter(crew__name="DeliveryCrew")
            
        if request.user.groups.filter(name="Customer").exists():
            orders = orders.filter(user=request.user)

        serializer = OrderSerializer(orders, many=True)
        return  Response({ "data": serializer.data ,"status": True, "message": 'Order saved'})
    def post(self, request):
        group = Group.objects.get(name='Unassigned')
        print(request.data.get('menu'))
        data = {
            "label": request.POST.get('label', 'Little Lemmon'),
            "user": request.user.id,
            "menu": request.data.get('menu'),
            "crew": group.id
        }
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return  Response({ "data": serializer.data ,"status": True, "message": 'Order saved'})
        return  Response({ "data": serializer.errors ,"status": True, "message": 'Order creation failed'})
