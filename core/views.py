from audioop import reverse
from django.contrib import messages
from django.db.models import Count
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
import paypalrestsdk
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from .models import Address, BlogPost, Cart, Category, Comuna, Country, Customer, NewsletterSubscription, OrderUpdate, Product, Order, OrderItem, Region, Review, Favorite, Report, Vendor, Comment
from .forms import AddressForm, CommentForm, CustomerRegistrationForm, CustomerProfileForm, OrderForm, OrderStatusForm, OrderStatusUpdateForm, OrderUpdateForm, ProductForm, ReviewForm, NewsletterSubscriptionForm, RoleAssignmentForm
from django.http import JsonResponse
from django.db.models import Q
import requests
from django.urls import reverse, reverse_lazy  
from django.views.generic import View, ListView, UpdateView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # Añadir esta línea
from .serializers import OrderSerializer, OrderItemSerializer
from .utils import reset_order_id_sequence
from .templatetags.custom_filters import multiply
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

class VendorProductListView(UserPassesTestMixin, ListView):
    model = Product
    template_name = 'app/vendor_product_list.html'

    def test_func(self):
        return self.request.user.customer.role == 'vendor'

@user_passes_test(lambda u: u.is_staff)
def assign_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    customer, created = Customer.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = RoleAssignmentForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('some_view_name')  # Redirigir a alguna vista después de asignar el rol
    else:
        form = RoleAssignmentForm(instance=customer)
    return render(request, 'app/assign_role.html', {'form': form, 'user': user})

class VendorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.customer.role == 'vendor' or self.request.user.is_staff

class IsVendorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Vendors').exists()

class IsCustomerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Customers').exists() or self.request.user.is_staff

def home(request):
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

@method_decorator(login_required, name='dispatch')
class OrderDetailView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)
        user_comments = Comment.objects.filter(order=order, user=request.user)
        user_reviews = Review.objects.filter(product__in=[item.product for item in order_items], user=request.user)
        
        # Crear un diccionario para verificar si el usuario ya ha dejado una reseña
        product_reviews_exist = {item.product.id: user_reviews.filter(product=item.product).exists() for item in order_items}
        
        return render(request, 'app/order_detail.html', {
            'order': order,
            'order_items': order_items,
            'user_comments': user_comments,
            'product_reviews_exist': product_reviews_exist,  # Pasar el diccionario al template
        })

    def post(self, request, order_id):
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        content = request.POST.get('content')
        rating = int(request.POST.get('rating'))
        comment_text = request.POST.get('comment')

        # Verificar si el usuario ya ha dejado un comentario
        if not Comment.objects.filter(order__id=order_id, user=request.user).exists():
            # Crear un comentario
            Comment.objects.create(
                user=request.user,
                order=get_object_or_404(Order, id=order_id),
                text=comment_text,
                verified=OrderItem.objects.filter(order__user=request.user, product=product).exists()
            )

        # Verificar si el usuario ya ha dejado una reseña para el producto
        if not Review.objects.filter(product=product, user=request.user).exists():
            # Crear una reseña
            Review.objects.create(
                user=request.user,
                product=product,
                content=content,
                rating=rating,
                verified=OrderItem.objects.filter(order__user=request.user, product=product).exists()
            )

        return redirect('order_detail', order_id=order_id)

    
class ProductDetail(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        reviews = Review.objects.filter(product=product)
        comments = Comment.objects.filter(order__items__product=product).distinct()
        user_favorite = None
        if request.user.is_authenticated:
            user_favorite = Favorite.objects.filter(user=request.user, product=product).first()
        
        # Calcula la calificación promedio
        total_rating = sum(review.rating for review in reviews)
        avg_rating = total_rating / len(reviews) if reviews else None
        
        return render(request, "app/productdetail.html", {
            'product': product,
            'reviews': reviews,
            'comments': comments,
            'user_favorite': user_favorite,
            'avg_rating': avg_rating,
        })

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
        # Obtener o crear el cliente con valores predeterminados
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={
                'name': request.user.username,
                'email': request.user.email,
                'locality': Country.objects.first(),  # Cambia esto según tus datos
                'city': 'Ciudad Predeterminada',      # Cambia esto según tus datos
                'mobile': '0000000000',               # Cambia esto según tus datos
                'zipcode': '0000000',                 # Cambia esto según tus datos
                'region': Region.objects.first(),     # Cambia esto según tus datos
                'comuna': Comuna.objects.first()      # Cambia esto según tus datos
            }
        )
        form = CustomerProfileForm(instance=customer)
        addresses = Address.objects.filter(user=request.user)
        return render(request, 'app/profile.html', {'form': form, 'addresses': addresses})

    def post(self, request):
        customer = get_object_or_404(Customer, user=request.user)
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente')
        else:
            messages.error(request, 'Error al actualizar el perfil')
        addresses = Address.objects.filter(user=request.user)
        return render(request, 'app/profile.html', {'form': form, 'addresses': addresses})

@login_required
def address(request):
    addresses = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': addresses})

class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        return render(request, 'app/address.html', {'addresses': addresses})

class AddAddressView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'app/add_address.html'
    success_url = '/address/'  # Redirige a la lista de direcciones

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def profile_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    order_details = []
    for order in orders:
        items = order.items.all()
        product_details = {
            item.product.title: {
                'quantity': item.quantity,
                'price': item.price,
                'subtotal': item.quantity * item.price,
                'item': item,
                'form': ReviewForm()
            } for item in items
        }
        order_details.append({'order': order, 'product_details': product_details})

    return render(request, 'app/profile_orders.html', {'order_details': order_details})

class UpdateAddressView(LoginRequiredMixin, View):
    def get(self, request, pk):
        address = get_object_or_404(Address, pk=pk)
        form = AddressForm(instance=address)
        return render(request, 'app/update_address.html', {'form': form, 'address': address})
    
    def post(self, request, pk):
        address = get_object_or_404(Address, pk=pk)
        form = AddressForm(request.POST, instance=address)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Dirección actualizada correctamente!')
            return redirect('address')
        else:
            messages.warning(request, 'No se ha podido actualizar la dirección!')
        return render(request, 'app/update_address.html', {'form': form, 'address': address})

class DeleteAddressView(LoginRequiredMixin, View):
    def get(self, request, pk):
        address = get_object_or_404(Address, pk=pk)
        address.delete()
        messages.success(request, 'Dirección eliminada correctamente')
        return redirect('profile')

def load_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(region_id=region_id).order_by('name')
    return JsonResponse(list(comunas.values('id', 'name')), safe=False)

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            cart_items = request.session.get('cart', [])
            for item in cart_items:
                product = Product.objects.get(id=item['product_id'])
                OrderItem.objects.create(order=order, product=product, quantity=item['quantity'], price=item['price'])

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
    for item in cart:
        price = item.product.discounted_price if item.product.discounted_price is not None else item.product.price
        total_amount += price * item.quantity

    context = {
        'cart': cart,
        'total_amount': total_amount,
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
        amount = sum(item.quantity * (item.product.discounted_price if item.product.discounted_price is not None else item.product.price) for item in cart)
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
        amount = sum(item.quantity * (item.product.discounted_price if item.product.discounted_price is not None else item.product.price) for item in cart)
        totalamount = amount + 40
        data = {'quantity': cart_product.quantity, 'amount': amount, 'totalamount': totalamount}
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cart_product = get_object_or_404(Cart, product_id=prod_id, user=request.user)
        cart_product.delete()
        cart = Cart.objects.filter(user=request.user)
        amount = sum(item.quantity * (item.product.discounted_price if item.product.discounted_price is not None else item.product.price) for item in cart)
        totalamount = amount + 40
        data = {'amount': amount, 'totalamount': totalamount}
        return JsonResponse(data)

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
                if item.product.discounted_price is not None:
                    totalamount += item.quantity * item.product.discounted_price
                else:
                    totalamount += item.quantity * item.product.price
            totalamount += shipping_amount

        # Crear el pedido y los elementos del pedido antes de redirigir a PayPal
        order = Order.objects.create(user=user, total_amount=totalamount, status='pending')
        for item in cart_items:
            price = item.product.discounted_price if item.product.discounted_price is not None else item.product.price
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=price)

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
        address = Address.objects.filter(user=user)
        
        totalamount = 0
        cart_product = [item for item in Cart.objects.all()
                        if item.user == user]
        
        if cart_product:
            for item in cart_product:
                if item.product.discounted_price:
                    totalamount += item.quantity * item.product.discounted_price
                else:
                    totalamount += item.quantity * item.product.price
        return render(request, 'app/checkout.html', {'cart_items': cart_items, 'address': address, 'totalamount': totalamount})

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
def admin_order_edit(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('admin_orders')
    else:
        form = OrderForm(instance=order)
    return render(request, 'app/admin_order_edit.html', {'form': form, 'order': order})

@staff_member_required
def admin_order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('admin_orders')
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

@method_decorator(login_required, name='dispatch')
class AddReview(View):
    def get(self, request, product_id, order_id):
        product = get_object_or_404(Product, id=product_id)
        form = ReviewForm()
        return render(request, 'app/add_review.html', {'form': form, 'product': product, 'order_id': order_id})

    def post(self, request, product_id, order_id):
        product = get_object_or_404(Product, id=product_id)
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.content = content
            review.rating = rating
            review.save()
            return redirect('order_detail', order_id=order_id)

        return render(request, 'app/add_review.html', {'form': form, 'product': product, 'order_id': order_id})


@login_required
def add_comment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.order = order
            comment.save()
            messages.success(request, 'Comentario añadido correctamente!')
        else:
            messages.error(request, 'Por favor, corrija los errores del formulario.')
    return redirect('order_detail', order_id=order_id)

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Pedido cancelado correctamente.')
    return redirect('profile_orders')

@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    messages.success(request, 'Producto añadido a favoritos!')
    return redirect('product_detail', pk=product_id)

@login_required
def remove_from_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite = Favorite.objects.filter(user=request.user, product=product).first()
    if favorite:
        favorite.delete()
        messages.success(request, 'Producto eliminado de favoritos!')
    return redirect('product_detail', pk=product_id)

@login_required
def report_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        if reason:
            Report.objects.create(user=request.user, product=product, reason=reason)
            messages.success(request, 'Producto reportado exitosamente!')
        else:
            messages.error(request, 'Por favor, proporciona una razón para el reporte.')
    return redirect('product_detail', pk=product_id)

@login_required
def product_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'app/product_reviews.html', {'reviews': reviews, 'product': product})

@login_required
def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    products = Product.objects.filter(vendor=vendor)
    return render(request, 'app/vendor_detail.html', {'vendor': vendor, 'products': products})

@login_required
def favorite_products(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'app/favorites.html', {'favorites': favorites})

class VendorView(View):
    def get(self, request, pk):
        vendor = get_object_or_404(Vendor, pk=pk)
        products = Product.objects.filter(vendor=vendor)
        return render(request, 'app/vendor_detail.html', {'vendor': vendor, 'products': products})

# Configuración de PayPal
def configure_paypal():
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()
    user_reviews = Review.objects.filter(user=request.user, product__in=[item.product for item in items])
    user_comments = Comment.objects.filter(user=request.user, order=order)
    order_updates = OrderUpdate.objects.filter(order=order).order_by('-update_date')
    is_admin = request.user.is_staff

    return render(request, 'app/order_detail.html', {
        'order': order,
        'order_items': items,
        'user_reviews': user_reviews,
        'user_comments': user_comments,
        'order_updates': order_updates,
        'is_admin': is_admin,
    })

@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderStatusUpdateForm(request.POST)
        if form.is_valid():
            order_update = form.save(commit=False)
            order_update.order = order
            order_update.save()
            order.status = form.cleaned_data['status']
            order.estimated_delivery_date = form.cleaned_data['estimated_delivery_date']
            order.save()
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderStatusUpdateForm(initial={'status': order.status, 'estimated_delivery_date': order.estimated_delivery_date})
    
    return render(request, 'app/update_order_status.html', {'form': form, 'order': order})


@login_required
def reviews(request):
    user_reviews = Review.objects.filter(user=request.user)
    review_statuses = []

    for review in user_reviews:
        order_item = review.product.orderitem_set.first()
        if order_item:
            order = order_item.order
            if order:
                if order.deleted:
                    review_statuses.append({'review': review, 'status': 'Reseña no existente'})
                else:
                    review_statuses.append({'review': review, 'status': 'Reseña válida'})
            else:
                review_statuses.append({'review': review, 'status': 'Reseña no existente'})
        else:
            review_statuses.append({'review': review, 'status': 'Reseña no existente'})

    return render(request, 'app/reviews.html', {'review_statuses': review_statuses})

# Vista para eliminar un pedido
@user_passes_test(lambda u: u.is_staff)
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.deleted = True  # Marca el pedido como eliminado
    order.save()
    messages.success(request, 'El pedido ha sido eliminado correctamente.')
    return redirect('admin_orders')


@staff_member_required
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'app/admin_orders.html', {'orders': orders})

# Vista para la lista de pedidos de administración

class VendorOrderListView(UserPassesTestMixin, ListView):
    model = Order
    template_name = 'app/vendor_orders.html'
    context_object_name = 'orders'

    def test_func(self):
        return self.request.user.groups.filter(name='Vendors').exists() or self.request.user.is_staff

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        vendor = Vendor.objects.get(user=self.request.user)
        return Order.objects.filter(items__product__vendor=vendor).distinct()

class EditOrderView(UserPassesTestMixin, UpdateView):
    model = Order
    fields = ['total_amount', 'status', 'estimated_delivery_date']
    template_name = 'app/edit_order.html'
    context_object_name = 'order'

    def get_success_url(self):
        if self.request.user.groups.filter(name='Vendors').exists():
            return reverse('vendor_orders')
        elif self.request.user.is_staff:
            return reverse('admin_orders')
        else:
            return reverse('profile_orders')

    def test_func(self):
        return self.request.user.groups.filter(name='Vendors').exists() or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = OrderItem.objects.filter(order=self.object)
        context['reviews'] = Review.objects.filter(product__in=[item.product for item in context['order_items']])
        context['comments'] = Comment.objects.filter(order=self.object)
        return context

class EditProductView(IsVendorMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'app/edit_product.html'
    context_object_name = 'product'
    success_url = reverse_lazy('vendor_product_list')  # Asegúrate de que esta URL esté definida en urls.py

    def test_func(self):
        product = self.get_object()
        return self.request.user.is_staff or product.vendor.user == self.request.user

class EditReviewView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.groups.filter(name='Vendors').exists()

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        form = ReviewForm(instance=review)
        return render(request, 'app/edit_review.html', {'form': form, 'review': review})

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('edit_order', pk=review.product.orderitem_set.first().order.id)
        return render(request, 'app/edit_review.html', {'form': form, 'review': review})



class EditCommentView(VendorRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'app/edit_comment.html'
    context_object_name = 'comment'
    success_url = reverse_lazy('vendor_orders')

    def test_func(self):
        review = self.get_object()
        return self.request.user.is_staff or review.product.vendor.user == self.request.user
    
class EditCommentView(UserPassesTestMixin, View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        form = CommentForm(instance=comment)
        return render(request, 'app/edit_comment.html', {'form': form, 'comment': comment})

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('edit_order', pk=comment.order.id)
        return render(request, 'app/edit_comment.html', {'form': form, 'comment': comment})

class DeleteReviewView(UserPassesTestMixin, View):
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        order_id = review.product.orderitem_set.first().order.id
        review.delete()
        return redirect('edit_order', pk=order_id)

class DeleteCommentView(UserPassesTestMixin, View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        order_id = comment.order.id
        comment.delete()
        return redirect('edit_order', pk=order_id)

@staff_member_required
def admin_order_search(request):
    query = request.GET.get('q')
    if query:
        orders = Order.objects.filter(id__icontains(query))
    else:
        orders = Order.objects.all()
    return render(request, 'app/admin_order_list.html', {'orders': orders})

# vista blog
class BlogListView(View):
    def get(self, request):
        posts = BlogPost.objects.all().order_by('-created_at')
        return render(request, 'app/blog_list.html', {'posts': posts})

class BlogDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        return render(request, 'app/blog_detail.html', {'post': post})
    
# vista noticias
class SubscribeNewsletterView(View):
    def post(self, request):
        email = request.POST.get('email')
        if email:
            if not NewsletterSubscription.objects.filter(email=email).exists():
                NewsletterSubscription.objects.create(email=email)
                messages.success(request, '¡Suscripción exitosa!')
            else:
                messages.warning(request, 'Este correo ya está suscrito.')
        else:
            messages.error(request, 'Por favor, ingrese un correo válido.')
        return redirect('home')

# vendor

class VendorProductListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Product
    template_name = 'app/vendor_product_list.html'
    context_object_name = 'products'

    def test_func(self):
        return self.request.user.groups.filter(name='Vendors').exists() or self.request.user.is_staff

    def get_queryset(self):
        if self.request.user.is_staff:
            return Product.objects.all()
        vendor = Vendor.objects.get(user=self.request.user)
        return Product.objects.filter(vendor=vendor)

class EditVendorProductView(IsVendorMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, vendor=request.user)
        form = ProductForm(instance=product)
        return render(request, 'app/edit_product.html', {'form': form, 'product': product})

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, vendor=request.user)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('vendor_product_list')
        return render(request, 'app/edit_product.html', {'form': form, 'product': product})
    
class AddProductView(IsVendorMixin, View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'app/edit_product.html', {'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.save()
            return redirect('vendor_product_list')
        return render(request, 'app/edit_product.html', {'form': form})