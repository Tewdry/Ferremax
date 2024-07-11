from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from rest_framework.routers import DefaultRouter
from .views import AddAddressView, AddReview, BlogDetailView, BlogListView, DeleteAddressView, DeleteCommentView, DeleteReviewView, EditCommentView, EditOrderView, EditProductView, EditReviewView, OrderViewSet, OrderItemViewSet, CategoryView, SubscribeNewsletterView, UpdateAddressView, VendorProductListView, admin_order_search, admin_orders, VendorOrderListView, delete_order, order_detail, product_reviews, reviews, update_order_status

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
    path('address/', views.AddressView.as_view(), name='address'),
    path('add-address/', AddAddressView.as_view(), name='add_address'),
    path('update-address/<int:pk>/', UpdateAddressView.as_view(), name='update_address'),
    path('delete-address/<int:pk>/', DeleteAddressView.as_view(), name='delete_address'),
    path('ajax/load-comunas/', views.load_comunas, name='ajax_load_comunas'),
    path('search/', views.search, name='search'),
    path('cart/', views.show_cart, name='show_cart'),

    # Carrito
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('confirm-order/', views.ConfirmOrder.as_view(), name='confirm_order'),

    path('minus-cart/', views.minus_cart, name='minus_cart'),
    path('plus-cart/', views.plus_cart, name='plus_cart'),
    path('remove-cart/', views.remove_cart, name='remove_cart'),

    # Autenticación
    path('registration/', views.CustomerRegistrationView.as_view(), name='customer_registration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('password-change/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html', success_url='/password-changedone'), name='password_change'),
    path('password-changedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='password_change_done'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html'), name='password_reset_confirm'),
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
    path('admin/orders/<int:order_id>/', views.admin_order_edit, name='admin_order_edit'),
    path('admin/orders/<int:order_id>/delete/', views.admin_order_delete, name='admin_order_delete'),
    path('admin-orders/', admin_orders, name='admin_orders'),
    path('admin-orders/search/', admin_order_search, name='admin_order_search'),
    path('order/<int:order_id>/update-status/', update_order_status, name='update_order_status'),
    path('order/<int:order_id>/delete/', delete_order, name='delete_order'),
    path('edit-order/<int:pk>/', EditOrderView.as_view(), name='edit_order'),
    path('edit-product/<int:pk>/', EditProductView.as_view(), name='edit_product'),
    path('edit-review/<int:review_id>/', EditReviewView.as_view(), name='edit_review'),
    path('delete-review/<int:review_id>/', DeleteReviewView.as_view(), name='delete_review'),
    path('edit-comment/<int:comment_id>/', EditCommentView.as_view(), name='edit_comment'),
    path('delete-comment/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('create_order/', views.create_order, name='create_order'),

    # Favoritos y reseñas
    path('favorites/', views.favorite_products, name='favorites'),
    path('add-to-favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('reviews/', reviews, name='reviews'),
    path('add-review/<int:product_id>/<int:order_id>/', AddReview.as_view(), name='add_review'),
    path('report-product/<int:product_id>/', views.report_product, name='report_product'),
    path('product-detail/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('product-reviews/<int:product_id>/', product_reviews, name='product_reviews'),
    path('add-comment/<int:order_id>/', views.add_comment, name='add_comment'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),

    # Vendedores
    path('vendor/orders/', VendorOrderListView.as_view(), name='vendor_orders'),

    #Statuts
    path('order-detail/<int:order_id>/', order_detail, name='order_detail'),
    path('order/<int:order_id>/update-status/', update_order_status, name='update_order_status'),

    # Vendedores
    path('vendor/<int:pk>/', views.VendorView.as_view(), name='vendor_detail'),
    path('vendors/<int:pk>/', views.VendorView.as_view(), name='vendor'),
    path('vendor/products/', VendorProductListView.as_view(), name='vendor_product_list'),
    path('order-detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),

    # Blog
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),

    # Boletín de noticias
    path('subscribe/', SubscribeNewsletterView.as_view(), name='subscribe_newsletter'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
