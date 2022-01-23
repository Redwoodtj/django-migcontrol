from django import template
from django.contrib.staticfiles import finders
from django.core.files.storage import FileSystemStorage
from sorl.thumbnail import get_thumbnail
from wagtail.core.models import Page
from wagtail.core.models import Site
from wagtail.core.templatetags.wagtailcore_tags import pageurl


register = template.Library()


@register.simple_tag(takes_context=True)
def slugurl_localized(context, slug):
    """
    A language-aware version of Wagtail's slugurl tag

    Returns the URL for the page that has the given slug.

    First tries to find a page on the current site. If that fails or a request
    is not available in the context, then returns the URL for the first page
    that matches the slug on any site.
    """
    page = None
    try:
        site = Site.find_for_request(context["request"])
        current_site = site
    except KeyError:
        # No site object found - allow the fallback below to take place.
        pass
    else:
        if current_site is not None:
            page = Page.objects.in_site(current_site).filter(slug=slug).first()

    # If no page is found, fall back to searching the whole tree.
    if page is None:
        page = Page.objects.filter(slug=slug).first()

    if page:
        # call pageurl() instead of page.relative_url() here so we get the ``accepts_kwarg`` logic
        return pageurl(context, page.localized)


class StaticPath(str):
    def __new__(cls, path: str, storage: FileSystemStorage):
        obj = super().__new__(cls, path)
        obj.storage = storage
        return obj


storage = FileSystemStorage(location="/")


@register.simple_tag(takes_context=False)
def get_static_thumbnail(file_: str, geometry, *args, **kwargs):
    disk_path = finders.find(file_)
    if disk_path:
        return get_thumbnail(
            StaticPath(disk_path, storage),
            geometry,
            *args,
            **kwargs,
        )
