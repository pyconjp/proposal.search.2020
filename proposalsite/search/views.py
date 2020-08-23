from django.shortcuts import render

from .models import Talk


def list_talks(request):
    talks = Talk.objects.all().order_by("sessionize_id")
    context = {"talks": talks}
    return render(request, "search/list_talks.html", context)
