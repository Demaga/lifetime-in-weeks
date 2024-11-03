from django import template

register = template.Library()


@register.filter
def map_weeks_to_events(events):
    """Convert a queryset of events into a set of week numbers"""
    return {event.week_number for event in events}


@register.filter
def multiply(value, arg):
    """Multiply the arg and value"""
    return int(value) * int(arg)
