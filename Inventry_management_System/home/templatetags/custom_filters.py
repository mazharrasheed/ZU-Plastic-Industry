from django import template

register = template.Library()

@register.filter(name='currency')
def currency(number):

    return "₨"+str(number)

@register.filter(name='multiply')
def multiply(item,qty):
    total_price=item*qty
    return total_price

@register.filter(name='rembal')
def rembal(item,qty):
    rem_balance=item-qty
    return  rem_balance

@register.filter(name='plus')
def plus(liabilitie,equity):
    rem_balance=liabilitie+equity
    return  rem_balance

@register.filter
def rembalance(balance, subtract_amount, add_increment):
    """Adjusts an account balance by subtracting a specific amount and adding an increment."""
    return balance - subtract_amount + add_increment


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)