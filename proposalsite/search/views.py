from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Talk


def _retrieve_page(paginator, get_request):
    page = get_request.get("page")
    page_obj = paginator.page(1)
    if page:
        page_obj = paginator.page(page)
    return page_obj


def list_talks(request):
    talks = Talk.objects.all().order_by("sessionize_id")

    paginator = Paginator(talks, settings.ITEM_PER_PAGE)
    page_obj = _retrieve_page(paginator, request.GET)

    context = {"page_obj": page_obj}
    return render(request, "search/list_talks.html", context)
