from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Address, Comuna, Country, Product, Region, Review, Comment, OrderUpdate, NewsletterSubscription

from .models import Customer,Order

class LoginForm(AuthenticationForm):
    username = UsernameField(label='Usuario',widget=forms.TextInput(attrs={'autofocus ':'True','class':'form-control'}))
    password = forms.CharField(label='Contraseña',widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'autofocus ':'True','class':'form-control'}))
    email = forms.EmailField(label='Correo Electronico', widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Antigua Contraseña', widget=forms.PasswordInput(attrs={'autofocus ':'True','autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput(attrs={'autofocus ':'True','autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={'autofocus ':'True','autocomplete':'current-password','class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Contraseña Nueva', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirmar Contraseña Nueva', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['profile_image', 'name', 'email', 'description', 'locality', 'city', 'mobile', 'zipcode', 'region', 'comuna']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(), required=True)

    class Meta:
        model = Review
        fields = ['content', 'rating']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'verified']

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = OrderUpdate
        fields = ['status', 'note']

class OrderStatusForm(forms.ModelForm):
    note = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = Order
        fields = ['status', 'estimated_delivery_date']

class OrderStatusUpdateForm(forms.ModelForm):
    estimated_delivery_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = OrderUpdate
        fields = ['status', 'estimated_delivery_date']

    def __init__(self, *args, **kwargs):
        super(OrderStatusUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar'))

class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'locality', 'city', 'mobile', 'zipcode', 'state', 'comuna']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'comuna': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comuna'].queryset = Comuna.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['comuna'].queryset = Comuna.objects.filter(region_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['comuna'].queryset = self.instance.state.comuna_set.order_by('name')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'vendor', 'title', 'description', 'price', 'discounted_price', 'product_image']


class RoleAssignmentForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['role']