from django.contrib import admin
from .models import Comment, Address, BlogCategory, BlogPost, Comuna, Customer, Favorite, NewsletterSubscription, OrderUpdate, Product, Category, Order, OrderItem, Region, Country, Report, Review, Vendor

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'discounted_price', 'product_image', 'vendor')
    search_fields = ('title', 'category__name')
    list_filter = ('category',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__title')

class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo', 'description')
    search_fields = ('name',)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'mobile', 'region', 'comuna')
    search_fields = ('user__username', 'name', 'email')
    list_filter = ('region', 'comuna')

    def region(self, obj):
        return obj.region.name
    region.admin_order_field = 'region'
    region.short_description = 'Region'

    def comuna(self, obj):
        return obj.comuna.name
    comuna.admin_order_field = 'comuna'
    comuna.short_description = 'Comuna'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'review_date', 'verified')
    list_filter = ('verified', 'rating', 'review_date')
    search_fields = ('user__username', 'product__title')
    actions = ['mark_as_verified']

    def mark_as_verified(self, request, queryset):
        queryset.update(verified=True)
    mark_as_verified.short_description = "Marcar como verificado"

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email', 'role']
    list_filter = ['role']
    search_fields = ['name', 'email']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address)
admin.site.register(Region)
admin.site.register(Country)
admin.site.register(Comuna)
admin.site.register(OrderUpdate)
admin.site.register(Favorite)
admin.site.register(Report)
admin.site.register(Comment)
admin.site.register(BlogCategory)
admin.site.register(BlogPost)
admin.site.register(NewsletterSubscription)
