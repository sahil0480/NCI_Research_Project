from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from .models import MenuItem
from django.core.exceptions import ObjectDoesNotExist
from .cart import Cart
import json

def index(request):
    return render(request, 'my_rest/index.html')

def reservation(request):
    return render(request, 'my_rest/reservation.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'my_rest/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'my_rest/login.html', {'form': form})
    
    
#######################################    

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import MenuItem
from .cart import Cart
import json

def menu(request):
    menu_items = MenuItem.objects.all()
    context = {'menu_items': menu_items}
    return render(request, 'my_rest/menu.html', context)

def add_to_cart(request, item_id):
    if request.method == 'POST':
        item = MenuItem.objects.get(id=item_id)
        cart_data = request.session.get('cart')
        if cart_data:
            cart = json.loads(cart_data)
        else:
            cart = []
        
        item_dict = {
            'id': item.id,
            'name': item.name,
            'price': str(item.price),
            'quantity': 1
        }
        cart.append(item_dict)
        request.session['cart'] = json.dumps(cart)
        return JsonResponse({'message': 'Item added to cart successfully'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)



def view_cart(request):
    cart_data = request.session.get('cart')
    if cart_data:
        cart = json.loads(cart_data)
    else:
        cart = []

    return render(request, 'my_rest/cart.html', {'cart': cart})


def remove_from_cart(request, item_id):
    if request.method == 'POST':
        try:
            item_id = int(item_id)
            cart = get_or_create_cart(request)
            cart.remove_item(item_id)
            request.session['cart'] = cart.to_json()
            return JsonResponse({'message': 'Item removed from cart successfully'})
        except ValueError:
            return JsonResponse({'error': 'Invalid item ID'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_or_create_cart(request):
    cart_data = request.session.get('cart')
    if cart_data:
        cart = Cart.from_json(cart_data)
    else:
        cart = Cart()
    return cart
    
    
def deserialize_cart(cart_data):
    return Cart.from_json(cart_data)