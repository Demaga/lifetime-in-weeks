from django import template

register = template.Library()


@register.filter
def map_events_to_weeks(events):
    """Convert a queryset of events into a set of week numbers"""
    return {event.week_number for event in events}


@register.simple_tag
def map_weeks_to_events(events, week_number):
    """Get all events for given week number"""
    filtered_events = []
    for event in events:
        if event.week_number == week_number:
            filtered_events.append(event)
    return filtered_events


@register.filter
def multiply(value, arg):
    """Multiply the arg and value"""
    return int(value) * int(arg)
