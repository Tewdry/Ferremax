from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def has_reviewed(product_id, product_reviews_exist):
    return product_reviews_exist.get(product_id, False)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()