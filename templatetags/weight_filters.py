# Import register from django template library
from django import template

# Import Decimal from decimal module
from decimal import Decimal

# Get the library's register object
register = template.Library()

@register.filter
def kg_to_lb(kg):
    # Conversion factor from kilograms to pounds
    kg_to_lb_conversion = Decimal('2.20462')
    return round(kg * kg_to_lb_conversion, 2)

@register.filter
def lb_to_kg(lb):
    # Conversion factor from pounds to kilograms
    lb_to_kg_conversion = Decimal('0.453592')
    return round(lb * lb_to_kg_conversion, 2)
