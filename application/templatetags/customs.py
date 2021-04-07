from django import template

register = template.Library()

@register.simple_tag
def canonical_tag(request):
    return request.build_absolute_uri(request.path)