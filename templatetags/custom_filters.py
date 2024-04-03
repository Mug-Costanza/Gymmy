from django import template

register = template.Library()

@register.filter
def format_large_number(value):
    if value >= 1000:
        return f'{value / 1000:.1f}k'
    else:
        return str(value)

