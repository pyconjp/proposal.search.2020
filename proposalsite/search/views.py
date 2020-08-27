from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from .models import Talk


def _filter_talks(talks, get_request):
    specified_only_english = get_request.get("only_english")
    if specified_only_english:
        talks = talks.filter(
            Q(speaking_language="en")
            | Q(slide_language="en")
            | Q(slide_language="bo")
        )
    category = get_request.get("category")
    if category:
        talks = talks.filter(category=category)
    return talks


def _retrieve_page(paginator, get_request):
    page = get_request.get("page")
    page_obj = paginator.page(1)
    if page:
        page_obj = paginator.page(page)
    return page_obj


def list_talks(request):
    talks = Talk.objects.all().order_by("sessionize_id")
    talks = _filter_talks(talks, request.GET)

    paginator = Paginator(talks, settings.ITEM_PER_PAGE)
    page_obj = _retrieve_page(paginator, request.GET)

    context = {"page_obj": page_obj, "categories": Talk.TalkCategory.values}
    return render(request, "search/list_talks.html", context)
