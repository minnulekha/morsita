from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import MyUSER,Restaurant,Customer,DeliveryPartner,MenuItem,Order,OrderItem,CartItem
from django.shortcuts import get_object_or_404
from collections import defaultdict
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect


# Create your views here.

def home_page(request):
    return render (request,"home.html")
def redirect_home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_home_page')  # Replace if needed
        elif request.user.usertype == 'restaurant':
            return redirect('restauranthome')
        elif request.user.usertype == 'customer':
            return redirect('customer_home_page')  # Create this view if not yet done
        elif request.user.usertype == 'delivery':
            return redirect('delivery_home_page')  # Create this view if not yet done
    return redirect('home_page')

def restaurant_register(request):
    if request.method == 'POST':
        rn = request.POST['restaurantname']
        on = request.POST['ownername']
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        em = request.POST['email']
        un = request.POST['username']
        p = request.POST['password']
        ad = request.POST['address']
        pin = request.POST['pincode']
        phn = request.POST['phone']
        lg = request.FILES['logo']  

        
        x = MyUSER.objects.create_user(
            first_name=fn,
            last_name=ln,
            email=em,
            username=un,
            password=p,
            usertype="restaurant",
            is_active=True,
            is_staff=True
        )
        x.save()

        
        y = Restaurant.objects.create(
            restaurant_id=x,   
            restaurant_name=rn,
            owner_name=on,
            address=ad,
            phone=phn,
            pincode=pin,
            logo=lg
        )
        y.save()

        return redirect (login_all)
    
    return render(request, "restaurant_reg.html")

def customer_register(request):
    if request.method == 'POST':
        
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        em = request.POST['email']
        un = request.POST['username']
        p = request.POST['password']
        ad = request.POST['address']
        pin = request.POST['pincode']
        phn = request.POST['phone']
         

        
        x = MyUSER.objects.create_user(
            first_name=fn,
            last_name=ln,
            email=em,
            username=un,
            password=p,
            usertype="customer",
            is_active=True,
            is_staff=False
        )
        x.save()

        
        y = Customer.objects.create(
            customer_id=x,   
            address=ad,
            phone=phn,
            pincode=pin,
            
        )
        y.save()

        return redirect (login_all)
    
    return render(request, "customer_reg.html")

def deliverypartner_register(request):
    if request.method == 'POST':
        vn = request.POST['vehiclenumber']
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        em = request.POST['email']
        un = request.POST['username']
        p = request.POST['password']
        ad = request.POST['address']
        phn = request.POST['phone']
        
        
        x = MyUSER.objects.create_user(
            first_name=fn,
            last_name=ln,
            email=em,
            username=un,
            password=p,
            usertype="delivery",
            is_active=True,
            is_staff=True
        )
        x.save()

        
        y = DeliveryPartner.objects.create(
            deliverypartner_id=x,   
            vehicle_number=vn,
            address=ad,
            phone=phn,
            
        )
        y.save()

        return redirect (login_all)
    
    return render(request, "deliverypartner_reg.html")

@login_required
def add_menu_item(request):
    restaurant = Restaurant.objects.get(restaurant_id=request.user)

    if request.method == 'POST':
        name = request.POST['item_name']
        desc = request.POST['description']
        price = request.POST['price']
        category = request.POST['category']
        image = request.FILES['item_image']
        available = 'is_available' in request.POST  # checkbox returns key if checked

        MenuItem.objects.create(
            restaurant=restaurant,
            item_name=name,
            description=desc,
            price=price,
            category=category,
            item_image=image,
            is_available=available
        )
        return redirect('restauranthome')

    return render(request, 'addmenu.html')

def login_all(request):
    if request.method == "POST":
        us = request.POST["username"]
        pas = request.POST['password']
        user = authenticate(request, username=us, password=pas)

        if user is not None:
            login(request, user)
            # 🔑 Refresh user object to ensure usertype is loaded
            request.user = MyUSER.objects.get(id=user.id)

            if user.is_superuser:
                return HttpResponse("Admin Login Successful")
                # return redirect("admin_home_page")

            elif user.usertype == 'restaurant':
                request.session['restaurant_id'] = user.id
                return redirect("restauranthome")

            elif user.usertype == 'customer':
                request.session['customer_id'] = user.id
                return redirect("customer_home_page")

            elif user.usertype == 'delivery':
                request.session['deliverypartner_id'] = user.id
                # return HttpResponse("Delivery Partner Login Successful")
                return HttpResponseRedirect(reverse('delivery_home_page'))

            else:
                return HttpResponse("Unknown user type")

        else:
            return HttpResponse("Invalid username or password")

    return render(request, "login_all.html")

def signup_page(request):
    return render(request, 'signup.html') 
def about_page(request):
    return render(request, 'about.html')
def help_page(request):
    return render(request, 'help.html') 

def restaurant_home_page(request):
    if not request.user.is_authenticated:
        return redirect('login') 

    restaurant = Restaurant.objects.get(restaurant_id=request.user)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)

    context = {
        'restaurant': restaurant,
        'menu_items': menu_items
    }

    return render(request, "res_page.html", context)

@login_required
def view_menu_items(request):
    if request.user.usertype != "restaurant":
        return redirect('login_all')  # or show error

    try:
        restaurant = Restaurant.objects.get(restaurant_id=request.user)
    except Restaurant.DoesNotExist:
        return redirect('login_all')

    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    
    return render(request, 'view_items.html', {
        'menu_items': menu_items,
        'restaurant': restaurant,
    })
@login_required
def edit_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id, restaurant__restaurant_id=request.user)

    if request.method == "POST":
        item.item_name = request.POST['item_name']
        item.description = request.POST['description']
        item.price = request.POST['price']
        item.category = request.POST['category']
        item.is_available = 'is_available' in request.POST

        if 'item_image' in request.FILES:
            item.item_image = request.FILES['item_image']

        item.save()
        return redirect('view_items')

    return render(request, 'editmenu.html', { 'item': item })

@login_required
def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id, restaurant__restaurant_id=request.user)
    item.delete()
    return redirect('view_items')

@login_required
def toggle_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id, restaurant__restaurant_id=request.user)
    item.is_available = not item.is_available
    item.save()
    return redirect('view_items')

@login_required
def restaurant_profile(request):
    if request.user.usertype != "restaurant":
        return redirect('login')

    restaurant = Restaurant.objects.get(restaurant_id=request.user)
    return render(request, 'restaurant_profile.html', {'restaurant': restaurant})

@login_required
def restaurant_settings(request):
    restaurant = Restaurant.objects.get(restaurant_id=request.user)

    if request.method == "POST":
        restaurant.restaurant_name = request.POST['restaurant_name']
        restaurant.owner_name = request.POST['owner_name']
        restaurant.phone = request.POST['phone']
        restaurant.address = request.POST['address']
        restaurant.pincode = request.POST['pincode']
        if 'logo' in request.FILES:
            restaurant.logo = request.FILES['logo']
        restaurant.save()
        return redirect('restaurant_settings')

    return render(request, 'restaurant_settings.html', {'restaurant': restaurant})

@login_required
def restaurant_orders(request):
    if request.user.usertype != 'restaurant':
        return redirect('login')

    restaurant = Restaurant.objects.get(restaurant_id=request.user)
    orders = Order.objects.filter(restaurant=restaurant).order_by('-created_at')

    status_choices = ['Pending', 'Confirmed', 'Out for delivery', 'Delivered', 'Cancelled']

    return render(request, 'restaurant_orders.html', {
        'restaurant': restaurant,
        'orders': orders,
        'status_choices': status_choices,
    })


from django.views.decorators.http import require_POST

@require_POST
@login_required
def update_order_status(request, order_id):
    if request.user.usertype != 'restaurant':
        return redirect('login')

    order = get_object_or_404(Order, id=order_id, restaurant__restaurant_id=request.user)
    new_status = request.POST.get('status')

    if new_status in ['Pending', 'Confirmed', 'Out for delivery', 'Delivered', 'Cancelled']:
        order.status = new_status
        order.save()

    return redirect('restaurant_orders')




# ------------------ CUSTOMER VIEWS ------------------

@login_required
def customer_home_page(request):
    if request.user.usertype != 'customer':
        return redirect('login')

    restaurants = Restaurant.objects.all()
    categories = ['biryani', 'pizzas', 'noodles', 'cakes', 'shake', 'khichdi']

    return render(request, 'customer_home.html', {
        'customer': request.user,
        'restaurants': restaurants,
        'categories': categories
    })

@login_required
def customer_view_menu(request, restaurant_id):
    if request.user.usertype != 'customer':
        return redirect('login')

    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant, is_available=True)

    return render(request, 'customer_menu_view.html', {
        'restaurant': restaurant,
        'menu_items': menu_items
    })

@csrf_exempt
@login_required
def add_to_cart(request, item_id):
    if request.method == 'POST' and request.user.usertype == 'customer':
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))

            if quantity < 1:
                return JsonResponse({'error': 'Quantity must be at least 1'}, status=400)

            customer = Customer.objects.get(customer_id=request.user)
            menu_item = MenuItem.objects.get(id=item_id)

            # Enforce one-restaurant-per-cart rule
            existing_cart_items = CartItem.objects.filter(customer=customer)
            if existing_cart_items.exists():
                existing_restaurant = existing_cart_items.first().menu_item.restaurant
                if existing_restaurant != menu_item.restaurant:
                    return JsonResponse({
                        'error': f'Cart already contains items from {existing_restaurant.restaurant_name}. Please clear your cart to add from another restaurant.'
                    }, status=400)

            cart_item, created = CartItem.objects.get_or_create(
                customer=customer,
                menu_item=menu_item
            )

            # Update quantity
            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()

            return JsonResponse({
                'message': f'{quantity} item{"s" if quantity > 1 else ""} added to cart',
                'total_quantity': cart_item.quantity
            }, status=200)

        except (json.JSONDecodeError, ValueError, MenuItem.DoesNotExist):
            return JsonResponse({'error': 'Invalid input or item'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def view_cart(request):
    if request.user.usertype != 'customer':
        return redirect('login')

    customer = Customer.objects.get(customer_id=request.user)
    cart_items = CartItem.objects.filter(customer=customer)

    grand_total = 0
    for item in cart_items:
        item.total_price = item.quantity * item.menu_item.price
        grand_total += item.total_price

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total
    })

@csrf_exempt
@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST' and request.user.usertype == 'customer':
        try:
            data = json.loads(request.body)
            new_qty = int(data.get('quantity', 1))
            cart_item = CartItem.objects.get(id=item_id, customer__customer_id=request.user)

            if new_qty < 1:
                cart_item.delete()
                return JsonResponse({'message': 'Item removed from cart.'})

            cart_item.quantity = new_qty
            cart_item.save()
            return JsonResponse({'message': 'Cart updated successfully.', 'total': cart_item.quantity * cart_item.menu_item.price})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def delete_cart_item(request, item_id):
    if request.method == 'POST' and request.user.usertype == 'customer':
        try:
            cart_item = CartItem.objects.get(id=item_id, customer__customer_id=request.user)
            cart_item.delete()
            return JsonResponse({'message': 'Item deleted from cart.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

import logging
logger = logging.getLogger(__name__)

@login_required
def customer_profile(request):
    logger.info(f"Logged in as: {request.user.username}, type: {getattr(request.user, 'usertype', 'unknown')}")

    if getattr(request.user, 'usertype', None) != 'customer':
        return redirect('login')

    customer = Customer.objects.get(customer_id=request.user)
    return render(request, 'customer_profile.html', {'customer': customer})

@login_required
def customer_settings(request):
    if not hasattr(request.user, 'usertype') or request.user.usertype != 'customer':
        return redirect('login_all')

    customer = Customer.objects.get(customer_id=request.user)

    if request.method == 'POST':
        customer.phone = request.POST.get('phone')
        customer.address = request.POST.get('address')
        customer.pincode = request.POST.get('pincode')
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()
        customer.save()
        return redirect('customer_settings')

    return render(request, 'customer_settings.html', {'customer': customer})

@login_required
def place_order(request):
    if request.user.usertype != 'customer':
        return redirect('login')

    customer = Customer.objects.get(customer_id=request.user)
    cart_items = CartItem.objects.filter(customer=customer)

    if not cart_items.exists():
        return redirect('view_cart')  # Or show message: "Cart is empty"

    restaurant = cart_items.first().menu_item.restaurant

    # Create order
    order = Order.objects.create(
        customer=customer,
        restaurant=restaurant,
        status='Pending'
    )

    # Add items to order
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            menu_item=item.menu_item,
            quantity=item.quantity
        )

    # Clear cart
    cart_items.delete()

    return render(request, 'order_success.html', {'order': order})

@login_required
def customer_orders(request):
    if request.user.usertype != 'customer':
        return redirect('login')

    customer = Customer.objects.get(customer_id=request.user)
    orders = Order.objects.filter(customer=customer).order_by('-created_at').prefetch_related('items__menu_item')

    return render(request, 'customer_orders.html', {
        'orders': orders,
        'customer': request.user
    })

# ------------------ Delivery VIEWS ------------------

@login_required
def delivery_home_page(request):
    if request.user.usertype != 'delivery':
        return redirect('login')

    delivery_partner = DeliveryPartner.objects.get(deliverypartner_id=request.user)
    
    # Orders assigned to this partner
    active_orders = Order.objects.filter(delivery_partner=delivery_partner).exclude(status='Delivered')

    # Orders not yet accepted by any partner
    available_orders = Order.objects.filter(delivery_partner__isnull=True).exclude(status='Delivered')

    return render(request, 'delivery_home.html', {
        'delivery_partner': delivery_partner,
        'active_orders': active_orders,
        'available_orders': available_orders
    })


@login_required
def delivery_profile(request):
    if request.user.usertype != 'delivery':
        return redirect('login')

    delivery_partner = DeliveryPartner.objects.get(deliverypartner_id=request.user)
    return render(request, 'delivery_profile.html', {'delivery_partner': delivery_partner})

@login_required
def delivery_settings(request):
    if request.user.usertype != 'delivery':
        return redirect('login')

    delivery_partner = DeliveryPartner.objects.get(deliverypartner_id=request.user)

    if request.method == 'POST':
        delivery_partner.phone = request.POST.get('phone')
        delivery_partner.vehicle_number = request.POST.get('vehicle_number')
        delivery_partner.address = request.POST.get('address')
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()
        delivery_partner.save()
        return redirect('delivery_settings')

    return render(request, 'delivery_settings.html', {'delivery_partner': delivery_partner})

from django.views.decorators.http import require_POST

@login_required
def accept_order(request, order_id):
    if request.user.usertype != 'delivery':
        return redirect('login')

    delivery_partner = DeliveryPartner.objects.get(deliverypartner_id=request.user)
    order = Order.objects.get(id=order_id)

    if order.delivery_partner is None:
        order.delivery_partner = delivery_partner
        order.status = "Accepted"  # ✅ just accepted, not yet out for delivery
        order.save()

    return redirect('delivery_home_page')

@require_POST
@login_required
@csrf_protect
def mark_out_for_delivery(request, order_id):
    if request.user.usertype != 'delivery':
        return redirect('login')

    delivery_partner = DeliveryPartner.objects.get(deliverypartner_id=request.user)
    order = get_object_or_404(Order, id=order_id, delivery_partner=delivery_partner)

    if order.status == 'Accepted':
        order.status = 'Out for delivery'
        order.save()

    return redirect('delivery_home_page')

@login_required
def mark_delivered(request, order_id):
    if request.user.usertype != 'delivery':
        return redirect('login')

    order = get_object_or_404(Order, id=order_id, delivery_partner__deliverypartner_id=request.user)

    if order.status == 'Out for delivery':
        order.status = 'Delivered'
        order.save()

    return redirect('delivery_home_page')

def logout_all(request):
    logout(request)
    return redirect (home_page)

@login_required
def debug_view(request):
    return HttpResponse(f"""
        <h1>DEBUG INFO</h1>
        <p><strong>Username:</strong> {request.user.username}</p>
        <p><strong>Is Authenticated:</strong> {request.user.is_authenticated}</p>
        <p><strong>User Type:</strong> {getattr(request.user, 'usertype', 'N/A')}</p>
        <p><strong>Is Staff:</strong> {request.user.is_staff}</p>
        <p><strong>Is Superuser:</strong> {request.user.is_superuser}</p>
        <p><strong>Session Keys:</strong> {list(request.session.keys())}</p>
    """)

