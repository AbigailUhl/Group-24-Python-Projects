import pandas as pd
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Player, WeatherRecord
from .forms import PlayerForm
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from django.http import HttpResponseNotAllowed


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
            "age_labels": json.dumps([]),
            "speed_values": json.dumps([]),
            "strength_values": json.dumps([]),
            "position_labels": json.dumps([]),
            "position_speed_values": json.dumps([]),
            "rating_labels": json.dumps([]),
            "rating_counts": json.dumps([]),
            "summary_stats": [],
        }
        return render(request, "myapp/analytics.html", context)

    df = df.dropna(subset=["age", "speed", "strength", "club_position", "rating"])

    age_data = (
        df.groupby("age")[["speed", "strength"]]
        .mean()
        .sort_index()
    )

    position_data = (
        df.groupby("club_position")
        .agg(
            player_count=("club_position", "count"),
            avg_speed=("speed", "mean")
        )
        .reset_index()
    )

    position_data = position_data[
        (position_data["club_position"] != "Sub") &
        (position_data["club_position"] != "Res")
    ]

    position_data = position_data[position_data["player_count"] >= 20]
    position_data = position_data.sort_values("avg_speed", ascending=False)

    rating_data = (
        df.groupby("rating")
        .size()
        .sort_index()
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
        "age_labels": json.dumps(age_data.index.tolist()),
        "speed_values": json.dumps([round(x, 2) for x in age_data["speed"].tolist()]),
        "strength_values": json.dumps([round(x, 2) for x in age_data["strength"].tolist()]),

        "position_labels": json.dumps(position_data["club_position"].tolist()),
        "position_speed_values": json.dumps([round(x, 2) for x in position_data["avg_speed"].tolist()]),

        "rating_labels": json.dumps(rating_data.index.tolist()),
        "rating_counts": json.dumps(rating_data.tolist()),

        "summary_stats": summary_stats,
    }

    return render(request, "myapp/analytics.html", context)

def weather_analytics(request):
    records = WeatherRecord.objects.values(
        "city",
        "date",
        "temperature_max",
        "temperature_min",
        "precipitation_sum",
    )

    df = pd.DataFrame(list(records))

    if df.empty:
        context = {
            "dates": json.dumps([]),
            "max_temps": json.dumps([]),
            "min_temps": json.dumps([]),
            "cities": json.dumps([]),
            "precipitation": json.dumps([]),
            "summary": [],
        }
        return render(request, "myapp/weather.html", context)

    temp_by_date = df.groupby("date")[["temperature_max", "temperature_min"]].mean().reset_index()
    precip_by_city = df.groupby("city")["precipitation_sum"].mean().reset_index()

    summary = [
        {
            "field": "Max Temperature",
            "count": int(df["temperature_max"].count()),
            "mean": round(df["temperature_max"].mean(), 2),
            "min": round(df["temperature_max"].min(), 2),
            "max": round(df["temperature_max"].max(), 2),
        },
        {
            "field": "Min Temperature",
            "count": int(df["temperature_min"].count()),
            "mean": round(df["temperature_min"].mean(), 2),
            "min": round(df["temperature_min"].min(), 2),
            "max": round(df["temperature_min"].max(), 2),
        },
    ]

    context = {
        "dates": json.dumps([str(date) for date in temp_by_date["date"]]),
        "max_temps": json.dumps(temp_by_date["temperature_max"].round(2).tolist()),
        "min_temps": json.dumps(temp_by_date["temperature_min"].round(2).tolist()),
        "cities": json.dumps(precip_by_city["city"].tolist()),
        "precipitation": json.dumps(precip_by_city["precipitation_sum"].round(2).tolist()),
        "summary": summary,
    }

    return render(request, "myapp/weather.html", context)


@staff_member_required
def fetch_data_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    call_command("fetch_data")
    return redirect("weather_analytics")