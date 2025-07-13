from django.urls import path
from .views import home_page,restaurant_register,customer_register,deliverypartner_register,login_all,logout_all,restaurant_home_page,signup_page,help_page,about_page,add_menu_item,view_menu_items,edit_menu_item,delete_menu_item,toggle_menu_item,redirect_home,restaurant_profile,restaurant_settings,customer_home_page,customer_view_menu,add_to_cart,view_cart,update_cart_item,delete_cart_item,customer_profile,debug_view,customer_settings,place_order,customer_orders,restaurant_orders,update_order_status,delivery_home_page, delivery_profile, delivery_settings,accept_order,mark_out_for_delivery,mark_delivered
urlpatterns=[
    path('',home_page),
    path('redirecthome/', redirect_home, name='redirect_home'),
    path('signup/restaurant',restaurant_register),
    path('customer/',customer_register, name='customer'),
    path('signup/delivery',deliverypartner_register),
    path('login/',login_all, name='login'),
    path('signup/', signup_page, name='signup'),
    path('help/', help_page, name='help'),
    path('about/', about_page, name='about'),
    path('logout', logout_all, name='logout'),
    path('restauranthome',restaurant_home_page, name='restauranthome'),
    path('addmenu/', add_menu_item, name='addmenu'),
    path('viewitems', view_menu_items, name='view_items'),
    path('editmenu/<int:item_id>/', edit_menu_item, name='edit_menu_item'),
    path('deletemenu/<int:item_id>/', delete_menu_item, name='delete_menu_item'),
    path('togglemenu/<int:item_id>/', toggle_menu_item, name='toggle_menu_item'),
    path('restaurant/profile/', restaurant_profile, name='restaurant_profile'),
    path('restaurant/settings/', restaurant_settings, name='restaurant_settings'),
    path('customerhome/', customer_home_page, name='customer_home_page'),
    path('restaurant/<int:restaurant_id>/menu/', customer_view_menu, name='customer_view_menu'),
    path('cart/add/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('cart/delete/<int:item_id>/', delete_cart_item, name='delete_cart_item'),
    path('customer/profile/', customer_profile, name='customer_profile'),
    path("debug/", debug_view, name="debug_view"),
    path('customer/settings/', customer_settings, name='customer_settings'),
    path('place-order/', place_order, name='place_order'),
    path('customer/orders/', customer_orders, name='customer_orders'),
    path('restaurant/orders/', restaurant_orders, name='restaurant_orders'),
    path('restaurant/orders/update/<int:order_id>/', update_order_status, name='update_order_status'),
    path('deliveryhome/', delivery_home_page, name='delivery_home_page'),
    path('delivery/profile/', delivery_profile, name='delivery_profile'),
    path('delivery/settings/', delivery_settings, name='delivery_settings'),
    path('delivery/accept/<int:order_id>/', accept_order, name='accept_order'),
    path('delivery/mark-out-for-delivery/<int:order_id>/', mark_out_for_delivery, name='mark_out_for_delivery'),
    path('delivery/mark-delivered/<int:order_id>/', mark_delivered, name='mark_delivered'),










    
]