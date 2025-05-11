from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter
def intdot(value):
    return intcomma(value).replace(",",".")