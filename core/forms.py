from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User

<<<<<<< HEAD
from .models import Customer,Order
=======
from .models import Customer
>>>>>>> 98aec02a70593aa42794e8f9f21285d80567ae6f

class LoginForm(AuthenticationForm):
    username = UsernameField(label='Usuario',widget=forms.TextInput(attrs=
    {'autofocus ':'True','class':'form-control'}))
    password = forms.CharField(label='Contraseña',widget=forms.PasswordInput(attrs=
    {'autocomplete':'current-password','class':'form-control'}))

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs=
    {'autofocus ':'True','class':'form-control'}))
    email = forms.EmailField(label='Correo Electronico', widget=forms.EmailInput(attrs=
    {'class':'form-control'}))
    password1 = forms.CharField(label='Contraseña', 
    widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.
    PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Antigua Contraseña', widget=forms.PasswordInput(attrs=
    {'autofocus ':'True','autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput(attrs=
    {'autofocus ':'True','autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(attrs=
    {'autofocus ':'True','autocomplete':'current-password','class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Contraseña Nueva', widget=forms.PasswordInput(attrs=
    {'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirmar Contraseña Nueva', widget=forms.PasswordInput(attrs=
    {'autocomplete':'current-password','class':'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields=['name','locality','city','mobile','state','zipcode']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
<<<<<<< HEAD
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
=======
        }
>>>>>>> 98aec02a70593aa42794e8f9f21285d80567ae6f
