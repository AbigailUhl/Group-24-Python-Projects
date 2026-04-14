from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Player


def home(request):
    return render(request, "myapp/home.html")


def record_list(request):
    records = Player.objects.all().order_by("id")

    paginator = Paginator(records, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "myapp/list.html", {"page_obj": page_obj})