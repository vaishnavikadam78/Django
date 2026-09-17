from django import template
from decimal import Decimal

register = template.Library()


@register.filter(name='currency')
def currency(value):
    try:
        float_value = float(value)
        return f"${float_value}"
    except (ValueError, TypeError):
        return value


@register.filter(name='discount')
def discount(value, percentage):

    value = Decimal(value)
    percentage = Decimal(percentage)

    return value - (value * (percentage / Decimal("100")))