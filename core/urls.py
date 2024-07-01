<<<<<<< HEAD
from django.urls import include, path
=======
from django.urls import path
>>>>>>> 98aec02a70593aa42794e8f9f21285d80567ae6f
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
<<<<<<< HEAD
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet, CategoryView
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path("", views.home, name="home"),
    path('api/', include(router.urls)),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path('category/<str:val>/', CategoryView.as_view(), name='category'),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name="product_detail"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('updateAddress/<int:pk>', views.UpdateAddress.as_view(), name='updateAddress'),
    path('search/', views.search, name='search'),
    path('cart/', views.show_cart, name='show_cart'),

    # Carrito
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.show_cart, name='show_cart'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('confirm-order/', views.ConfirmOrder.as_view(), name='confirm_order'),

    path('minus-cart/', views.minus_cart, name='minus_cart'),
    path('plus-cart/', views.plus_cart, name='plus_cart'),
    path('remove-cart/', views.remove_cart, name='remove_cart'),

    # Autenticación
    path('registration/', views.CustomerRegistrationView.as_view(), name='customer_registration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('password-change/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm, success_url='/password-changedone'), name='password_change'),
    path('password-changedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='password_change_done'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    # API
    path('convert-currency/', views.convert_currency, name='convert_currency'),
    path('api-view/', views.api_data_view, name='api_view'),

    # PayPal
    path("payment/", views.Payment.as_view(), name="payment"),
    path("app/execute/", views.ExecutePayment.as_view(), name="payment_execute"),
    path("app/cancel/", views.CancelPayment.as_view(), name="payment_cancel"),

    # Pedidos
    path('profile/orders/', views.profile_orders, name='profile_orders'),
    path('payment-completed/', views.payment_completed, name='payment_completed'),
    path('api/my-orders/', views.my_orders, name='my_orders'),

    # Administrar órdenes
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),
    path('admin/orders/<int:order_id>/', views.admin_order_edit, name='admin_order_edit'),
    path('admin/orders/<int:order_id>/delete/', views.admin_order_delete, name='admin_order_delete'),

    path('create_order/', views.create_order, name='create_order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm

urlpatterns = [
    path("", views.home),
    path("about/", views.about,name="about"),
    path("contact/", views.contact,name="contact"),
    path("category/<slug:val>", views.CategoryView.as_view(),name="category"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(),name="product-detail"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name='updateAddress'),

    #Carrito
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),



    #Autenticación
    path('registration/', views.CustomerRegistrationView.as_view(),name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm) , name='login'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name
    ='app/changepassword.html', form_class=MyPasswordChangeForm, 
    success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name=
    'app/passwordchangedone.html'), name='passwordchangedone'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name=
    'app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name=
    'app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view
    (template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view
    (template_name='app/password_reset_complete.html'), name='password_reset_complete'),


    #api
    path('convert-currency/', views.convert_currency, name='convert_currency'),
    path('api/', views.api_view, name='api_view'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 98aec02a70593aa42794e8f9f21285d80567ae6f
