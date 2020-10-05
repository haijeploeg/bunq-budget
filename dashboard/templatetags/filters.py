from django import template

register = template.Library()

@register.filter(name='get')
def get(dictionary, key):
    try:
        return dictionary[key]
    except KeyError:
        return ''


@register.filter(name='monetary_type')
def monetary_type(value):
    human_monetary_type = {
        'MB': 'Rekening',
        'MJ': 'Gezamenlijk',
        'MS': 'Spaar'
    }
    try:
        return human_monetary_type[value]
    except KeyError:
        return ''
