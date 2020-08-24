from django import template

register = template.Library()


@register.simple_tag
def add_query_to_request(request, field, value):
    url_dict = request.GET.copy()
    url_dict[field] = value
    return url_dict.urlencode()


@register.filter(is_safe=True)
def parse_search_parameter(query_dict, key):
    value = query_dict.get(key)
    return value if value else ""
