import csv
from pathlib import Path
from datetime import datetime

from django.core.management.base import BaseCommand
from myapp.models import Player, Country, Team


class Command(BaseCommand):
    help = "Load FIFA player data from CSV into the database"

    def handle(self, *args, **kwargs):
        csv_path = Path("data/raw/cleaned_players.csv")

        if not csv_path.exists():
            self.stdout.write(self.style.ERROR(f"CSV file not found: {csv_path}"))
            return

        # Clear old data (optional but recommended for clean runs)
        Player.objects.all().delete()
        Team.objects.all().delete()
        Country.objects.all().delete()

        with open(csv_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            count = 0

            for row in reader:
                # --- Country ---
                country_name = row.get("Nationality", "Unknown").strip()
                country_obj, _ = Country.objects.get_or_create(name=country_name)

                # --- Team ---
                team_name = row.get("Club", "Unknown").strip()
                team_obj, _ = Team.objects.get_or_create(name=team_name)

                # --- Convert birth date safely ---
                birth_date = None
                if row.get("Birth_Date"):
                    try:
                        birth_date = datetime.strptime(row["Birth_Date"], "%Y-%m-%d").date()
                    except:
                        birth_date = None

                # --- Player level (must match choices) ---
                level = row.get("Player_Level", "")
                if level not in ["Elite", "Top", "Mid", "Low"]:
                    level = ""

                # --- Create Player ---
                Player.objects.create(
                    name=row.get("Name", "").strip(),
                    nationality=country_obj,
                    team=team_obj,

                    national_position=row.get("National_Position", "").strip(),
                    club_position=row.get("Club_Position", "").strip(),

                    rating=int(row.get("Rating") or 0),
                    height=float(row.get("Height") or 0) if row.get("Height") else None,
                    weight=float(row.get("Weight") or 0) if row.get("Weight") else None,
                    birth_date=birth_date,
                    age=int(row.get("Age") or 0),

                    skill_moves=int(row.get("Skill_Moves") or 0) if row.get("Skill_Moves") else None,
                    ball_control=int(row.get("Ball_Control") or 0) if row.get("Ball_Control") else None,
                    dribbling=int(row.get("Dribbling") or 0) if row.get("Dribbling") else None,
                    speed=int(row.get("Speed") or 0) if row.get("Speed") else None,
                    strength=int(row.get("Strength") or 0) if row.get("Strength") else None,

                    player_level=level,
                )

                count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {count} players"))