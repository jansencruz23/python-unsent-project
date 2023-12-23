from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name='time_ago')
def time_ago(value):
    time_difference = timezone.now() - value

    intervals = [
        ("year", 31536000),
        ("month", 2592000),
        ("week", 604800),
        ("day", 86400),
        ("hour", 3600),
        ("minute", 60),
    ]

    for name, seconds in intervals:
        count = time_difference.total_seconds() // seconds
        if count > 0:
            if count == 1:
                return f"1 {name} ago"
            else:
                return f"{int(count)} {name}s ago"

    return "Just now"