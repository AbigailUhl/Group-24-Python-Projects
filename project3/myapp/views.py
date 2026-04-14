from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Player
from .forms import PlayerForm

def home(request):
    return render(request, "myapp/home.html")

def record_list(request):
    records = Player.objects.all().order_by("id")
    paginator = Paginator(records, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "myapp/list.html", {"page_obj": page_obj})

def record_detail(request, pk):
    record = get_object_or_404(Player, pk=pk)
    return render(request, "myapp/detail.html", {"record": record})

def record_add(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            record = form.save()
            return redirect("record_detail", pk=record.pk)
    else:
        form = PlayerForm()

    return render(request, "myapp/form.html", {"form": form, "title": "Add Player"})

def record_edit(request, pk):
    record = get_object_or_404(Player, pk=pk)

    if request.method == "POST":
        form = PlayerForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save()
            return redirect("record_detail", pk=record.pk)
    else:
        form = PlayerForm(instance=record)

    return render(request, "myapp/form.html", {"form": form, "title": "Edit Player"})

def record_delete(request, pk):
    record = get_object_or_404(Player, pk=pk)

    if request.method == "POST":
        record.delete()
        return redirect("record_list")

    return render(request, "myapp/confirm_delete.html", {"record": record})