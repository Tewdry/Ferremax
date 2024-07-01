<<<<<<< HEAD
from audioop import reverse
from django.contrib import messages
from django.db.models import Count
from django.conf import settings
import paypalrestsdk
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Cart, Category, Customer, Product, Order, OrderItem
from .forms import CustomerRegistrationForm, CustomerProfileForm, OrderForm
from django.http import JsonResponse
from django.db.models import Q
import requests
from django.urls import reverse  
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .serializers import OrderSerializer, OrderItemSerializer
from .utils import reset_order_id_sequence
from .templatetags.custom_filters import multiply
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
=======
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View
from . models import Cart, Customer, Product
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.http import JsonResponse
from django.db.models import Q
import requests
from transbank.webpay.webpay_plus.transaction import Transaction
>>>>>>> 98aec02a70593aa42794e8f9f21285d80567ae6f

# Create your views here.

def home(request):
<<<<<<< HEAD
    return render(request, "app/home.html")

def about(request):
    return render(request, "app/about.html")

def contact(request):
    return render(request, "app/contact.html")

class CategoryView(View):
    def get(self, request, val):
        category = get_object_or_404(Category, name=val)
        products = Product.objects.filter(category=category)
        titles = Product.objects.filter(category=category).values('title')
        return render(request, "app/category.html", {'category': category, 'products': products, 'titles': titles})


class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html", locals())

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", locals())
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario Creado Correctamente!")
        else:
            messages.warning(request, "No se ha podido crear el Usuario")
        return render(request, "app/customerregistration.html", locals())

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())
    
    def post(self, request):
=======
    return render(request,"app/home.html")

def about(request):
    return render(request,"app/about.html")

def contact(request):
    return render(request,"app/contact.html")

class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())
    
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,"app/productdetail.html",locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,"app/customerregistration.html",locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Usuario Creado Correctamente!")
        else:
            messages.warning(request,"No se ha podido crear el Usuario")
        return render(request,"app/customerregistration.html",locals())
    
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self,request):
>>>>>>> 98aec02a70593aa42794e8f9f21285d80567ae6f
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

<<<<<<< HEAD
            reg = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile,
                           state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Perfil guardado correctamente!')
        else:
            messages.warning(request, "No se ha podido guardar el perfil!")
        return render(request, 'app/profile.html', locals())

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())

@login_required
def profile_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    order_details = []
    for order in orders:
        items = order.items.all()  # Utilizando el related_name 'items'
        product_details = {item.product.title: {'quantity': item.quantity, 'price': item.price, 'subtotal': item.quantity * item.price, 'item': item} for item in items}
        order_details.append({'order': order, 'product_details': product_details})

    return render(request, 'app/profile_orders.html', {'order_details': order_details})

class UpdateAddress(LoginRequiredMixin, View):
    def get(self, request, pk):
        add = get_object_or_404(Customer, pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', locals())
    
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = get_object_or_404(Customer, pk=pk)
=======
            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,
                            state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Perfil guardado correctamente!')
        else:
            messages.warning(request,"No se ha podido guardar el perfil!")
        return render(request, 'app/profile.html',locals())
    
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',locals())

class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
>>>>>>> 98aec02a70593aa42794e8f9f21285d80567ae6f
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
<<<<<<< HEAD
            messages.success(request, "Perfil actualizado correctamente!")
        else:
            messages.warning(request, "No se ha podido actualizar el perfil!")
        return redirect("address")

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            print("Order created:", order.id)
            
            cart_items = request.session.get('cart', [])
            print("Cart items:", cart_items)
            for item in cart_items:
                product = Product.objects.get(id=item['product_id'])
                OrderItem.objects.create(order=order, product=product, quantity=item['quantity'], price=item['price'])
                print(f"Added item {item['product_id']} to order {order.id}")

            request.session['cart'] = []  # Clear the cart after order is created
            return redirect('profile_orders')
    else:
        form = OrderForm()
    
    return render(request, 'create_order.html', {'form': form})

@login_required
def add_to_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = get_object_or_404(Product, id=prod_id)
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart.quantity += 1
        cart.save()
        return redirect('show_cart')

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    total_amount = 0
    total_items = 0
    for item in cart:
        total_amount += item.product.discounted_price * item.quantity
        total_items += item.quantity
    context = {
        'cart': cart,
        'totalamount': total_amount,
        'totalitems': total_items,
    }
    return render(request, 'app/addtocart.html', context)

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cart_product = get_object_or_404(Cart, product_id=prod_id, user=request.user)
        cart_product.quantity += 1
        cart_product.save()
        cart = Cart.objects.filter(user=request.user)
        amount = sum(item.quantity * item.product.discounted_price for item in cart)
        totalamount = amount + 40
        data = {'quantity': cart_product.quantity, 'amount': amount, 'totalamount': totalamount}
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cart_product = get_object_or_404(Cart, product_id=prod_id, user=request.user)
        if cart_product.quantity > 1:
            cart_product.quantity -= 1
            cart_product.save()
        cart = Cart.objects.filter(user=request.user)
        amount = sum(item.quantity * item.product.discounted_price for item in cart)
        totalamount = amount + 40
        data = {'quantity': cart_product.quantity, 'amount': amount, 'totalamount': totalamount}
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cart_products = Cart.objects.filter(product_id=prod_id, user=request.user)
        cart_products.delete()
        cart = Cart.objects.filter(user=request.user)
        amount = sum(item.quantity * item.product.discounted_price for item in cart)
        totalamount = amount + 40
        data = {'amount': amount, 'totalamount': totalamount}
        return JsonResponse(data)
=======
            messages.success(request,"Perfil actualizado correctamente!")
        else:
            messages.warning(request,"No se ha podido actualizar el perfil!")
        return redirect("address")

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount * value
    totalamount = amount * 40
    return render(request, 'app/addtocart.html',locals())

class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        return render(request, 'app/checkout.html',locals())
    
def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

>>>>>>> 98aec02a70593aa42794e8f9f21285d80567ae6f

def convert_currency(request):
    if request.method == 'GET':
        amount = request.GET.get('amount')
        from_currency = request.GET.get('from_currency')
        to_currency = request.GET.get('to_currency')

        if not amount or not from_currency or not to_currency:
            return JsonResponse({'error': 'Missing parameters'}, status=400)

        try:
            amount = float(amount)
        except ValueError:
            return JsonResponse({'error': 'Invalid amount'}, status=400)

<<<<<<< HEAD
        # Valores iniciales de las monedas
        from_rate = 1
        to_rate = 1

        # Obtener la tasa de conversión desde `from_currency`
        api_url_from = f'https://mindicador.cl/api/{from_currency}'
        response_from = requests.get(api_url_from)
        if response_from.status_code == 200:
            data_from = response_from.json()
            if from_currency == 'clp':
                from_rate = 1
            else:
                from_rate = data_from['serie'][0]['valor']
        else:
            return JsonResponse({'error': 'Failed to fetch exchange rates from from_currency'}, status=500)

        # Obtener la tasa de conversión a `to_currency`
        api_url_to = f'https://mindicador.cl/api/{to_currency}'
        response_to = requests.get(api_url_to)
        if response_to.status_code == 200:
            data_to = response_to.json()
            if to_currency == 'clp':
                to_rate = 1
            else:
                to_rate = data_to['serie'][0]['valor']
        else:
            return JsonResponse({'error': 'Failed to fetch exchange rates from to_currency'}, status=500)

        # Calcular el resultado de la conversión
        result = (amount * from_rate) / to_rate
        return JsonResponse({'result': f"{result:,.2f}"})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def api_data_view(request):
    api_url = 'https://mindicador.cl/api'
    response = requests.get(api_url)
    data = {}
    if response.status_code == 200:
        data = response.json()
    return render(request, 'app/api_view.html', {'data': data})

def configure_paypal():
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET
    })

class Payment(View):
    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        totalamount = 0
        shipping_amount = 150  # Example shipping cost

        if cart_items:
            for item in cart_items:
                totalamount += item.quantity * item.product.discounted_price
            totalamount += shipping_amount

        # Crear el pedido y los elementos del pedido antes de redirigir a PayPal
        order = Order.objects.create(user=user, total_amount=totalamount, status='pending')
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.discounted_price)

        # Configuración de PayPal
        paypalrestsdk.configure({
            "mode": "sandbox",  # Cambiar a "live" en producción
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": str(totalamount),
                    "currency": "USD"
                },
                "description": "Compra en Ferremas"
            }],
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('payment_execute')),
                "cancel_url": request.build_absolute_uri(reverse('payment_cancel'))
            }
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    # Guardar el ID de la transacción de PayPal en el pedido
                    order.paypal_payment_id = payment.id
                    order.save()
                    return redirect(approval_url)
        else:
            return render(request, 'app/error.html', {'error': payment.error})


class ExecutePayment(View):
    def get(self, request):
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')

        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            user = request.user
            # Buscar el pedido con el ID de la transacción de PayPal
            order = Order.objects.get(paypal_payment_id=payment_id, user=user)
            order.status = 'completed'
            order.save()

            # Borrar los elementos del carrito
            Cart.objects.filter(user=user).delete()

            return render(request, 'app/success.html', {'order': order})
        else:
            return render(request, 'app/error.html', {'error': payment.error})


class Checkout(View):
    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        address = Customer.objects.filter(user=user)
        totalamount = 0
        shipping_amount = 150  # Example shipping cost

        if cart_items:
            for item in cart_items:
                totalamount += item.quantity * item.product.discounted_price
            totalamount += shipping_amount

        return render(request, 'app/confirm_order.html', {'address': address, 'cart_items': cart_items, 'totalamount': totalamount})

class ConfirmOrder(View):
    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        famount = sum(item.quantity * item.product.discounted_price for item in cart_items)
        totalamount = famount + 40
        address = Customer.objects.filter(user=user)

        # Crea la orden y guarda los items del carrito
        if cart_items.exists():
            order = Order.objects.create(user=user, total_amount=totalamount)
            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.discounted_price)
            # Limpiar el carrito
            cart_items.delete()

        context = {
            'cart_items': cart_items,
            'totalamount': totalamount,
            'address': address,
        }
        return render(request, 'app/confirm_order.html', context)

@csrf_exempt
def payment_completed(request):
    if request.method == 'POST':
        data = request.POST
        order_id = data.get('orderID')
        user_id = request.user.id
        order = Order.objects.get(id=order_id, user_id=user_id)
        order.status = 'completed'
        order.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

@api_view(['GET'])
def my_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@staff_member_required
def admin_order_list(request):
    orders = Order.objects.all()
    return render(request, 'app/admin_order_list.html', {'orders': orders})

@staff_member_required
def admin_order_edit(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('admin_order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'app/admin_order_edit.html', {'form': form, 'order': order})

@staff_member_required
def admin_order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('admin_order_list')
    return render(request, 'app/admin_order_delete.html', {'order': order})

class CancelPayment(View):
    def get(self, request):
        return render(request, 'app/cancel.html')
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(title__icontains=query)
    return render(request, 'app/search_results.html', {'products': products})
=======
        api_url = f'https://mindicador.cl/api/{from_currency}'
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            if 'serie' in data:
                from_rate = data['serie'][0]['valor']
                to_rate = data['serie'][0]['valor']
                if from_currency != 'uf':
                    to_rate = requests.get(f'https://mindicador.cl/api/{to_currency}').json()['serie'][0]['valor']
                result = (amount / from_rate) * to_rate
                return JsonResponse({'result': result})
            else:
                return JsonResponse({'error': 'Invalid currency'}, status=400)
        else:
            return JsonResponse({'error': 'Failed to fetch exchange rates'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def api_view(request):
    api_url = 'https://mindicador.cl/api'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        
        # Lógica para convertir los datos de la API a otra moneda
        # Supongamos que queremos convertir el valor del dólar a pesos chilenos
        if 'dolar' in data:
            dolar_value = data['dolar']['valor']
            converted_value = dolar_value * 800 # Supongamos que 1 dólar equivale a 800 pesos chilenos
            data['dolar']['valor'] = converted_value
        
        return render(request, 'app/api_view.html', {'data': data})
    else:
        return JsonResponse({'error': 'Failed to fetch data from API'}, status=500)
    

def create_transaction(request):
    # Lógica para crear la transacción en Transbank
    # Aquí puedes utilizar el SDK de Transbank para crear la transacción

    # Después de crear la transacción, redirigir al usuario a la página de Transbank
    return redirect('https://www.transbank.cl/')  # Reemplaza con la URL de Transbank
>>>>>>> 98aec02a70593aa42794e8f9f21285d80567ae6f
