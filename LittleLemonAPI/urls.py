from django.urls import path
from .views import MenuItem, MenuList, CategoryList, OrderList, update_orders_status, assign_orders_to_delivery, assign_user_to_group, get_orders_by_group
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('login/', obtain_auth_token, name='user_login'),
    path('menu-items/', MenuList.as_view(), name='menu_list'),
    path('menu-items/<int:pk>/', MenuItem.as_view(), name='menu_item'),
    path('category/', CategoryList.as_view(), name='CategoryList'),
    path('orders/', OrderList.as_view(), name='OrderList'),
    path('orders/group', get_orders_by_group, name='order_list'),
    path('orders/<int:pk>/assign/', assign_orders_to_delivery, name='assign_orders_to_delivery'),
    path('orders/<int:pk>/status/', update_orders_status, name='update_orders_status'),
    path('groups/', assign_user_to_group, name='users_groups'),
 
]
