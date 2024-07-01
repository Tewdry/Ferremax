from django.db import models
from django.contrib.auth.models import User

<<<<<<< HEAD
STATE_CHOICES = (
    ('Santiago', 'Buin'),
    ('Concepcion', 'Chillan'),
    ('Temuco', 'Villarica'),
    ('Arica', 'Antofagasta'),
    ('Valparaiso', 'Viña del Mar'),
)

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
=======
# Create your models here.

STATE_CHOICES = (
    ('Santiago','Buin'),
    ('Concepcion','Chillan'),
    ('Temuco','Villarica'),
    ('Arica','Antofagasta'),
    ('Valparaiso','Viña del Mar'),
)

CATEGORY_CHOICES=(
    ('HR','Herramientas Manuales'),
    ('MB','Materiales Básicos'),
    ('SG','Equipos de Seguridad'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
>>>>>>> 98aec02a70593aa42794e8f9f21285d80567ae6f
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)
<<<<<<< HEAD

=======
>>>>>>> 98aec02a70593aa42794e8f9f21285d80567ae6f
    def __str__(self):
        return self.name

class Cart(models.Model):
<<<<<<< HEAD
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
=======
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
>>>>>>> 98aec02a70593aa42794e8f9f21285d80567ae6f
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
<<<<<<< HEAD
        return self.quantity * self.product.discounted_price

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    paypal_payment_id = models.CharField(max_length=100, blank=True, null=True)  # Agregar este campo

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"
=======
        return self.quantity * self.product.discounted_price
>>>>>>> 98aec02a70593aa42794e8f9f21285d80567ae6f
