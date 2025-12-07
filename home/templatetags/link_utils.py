from urllib.parse import urlsplit

from django import template

register = template.Library()


@register.filter
def strip_domain(url: str) -> str:
    """
    Remove scheme + netloc from a URL, keep path/query/fragment.
    Useful to force links to stay relative even if the CMS stores absolute URLs.
    """
    if not url:
        return ""
    parts = urlsplit(url)
    if not parts.scheme and not parts.netloc:
        return url
    path = parts.path or "/"
    query = f"?{parts.query}" if parts.query else ""
    fragment = f"#{parts.fragment}" if parts.fragment else ""
    return f"{path}{query}{fragment}"
