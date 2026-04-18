import pandas as pd
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

    return render(request, "myapp/form.html", {"form": form})


def record_edit(request, pk):
    record = get_object_or_404(Player, pk=pk)

    if request.method == "POST":
        form = PlayerForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save()
            return redirect("record_detail", pk=record.pk)
    else:
        form = PlayerForm(instance=record)

    return render(request, "myapp/form.html", {"form": form})


def record_delete(request, pk):
    record = get_object_or_404(Player, pk=pk)

    if request.method == "POST":
        record.delete()
        return redirect("record_list")

    return render(request, "myapp/confirm_delete.html", {"record": record})


def analytics(request):
    records = Player.objects.values(
        "age",
        "speed",
        "strength",
        "club_position",
        "rating",
    )

    df = pd.DataFrame(list(records))

    if df.empty:
        context = {
            "age_labels": [],
            "speed_values": [],
            "strength_values": [],
            "position_labels": [],
            "position_speed_values": [],
            "summary_stats": [],
        }
        return render(request, "myapp/analytics.html", context)

    df = df.dropna(subset=["age", "speed", "strength", "club_position", "rating"])

    age_data = df.groupby("age")[["speed", "strength"]].mean().sort_index()

    position_data = (
        df.groupby("club_position")["speed"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    summary_stats = [
        {
            "field": "Rating",
            "count": int(df["rating"].count()),
            "mean": round(df["rating"].mean(), 2),
            "min": int(df["rating"].min()),
            "max": int(df["rating"].max()),
        },
        {
            "field": "Speed",
            "count": int(df["speed"].count()),
            "mean": round(df["speed"].mean(), 2),
            "min": int(df["speed"].min()),
            "max": int(df["speed"].max()),
        },
        {
            "field": "Strength",
            "count": int(df["strength"].count()),
            "mean": round(df["strength"].mean(), 2),
            "min": int(df["strength"].min()),
            "max": int(df["strength"].max()),
        },
    ]

    context = {
        "age_labels": list(age_data.index),
        "speed_values": [round(x, 2) for x in age_data["speed"]],
        "strength_values": [round(x, 2) for x in age_data["strength"]],
        "position_labels": list(position_data.index),
        "position_speed_values": [round(x, 2) for x in position_data.values],
        "summary_stats": summary_stats,
    }

    return render(request, "myapp/analytics.html", context)