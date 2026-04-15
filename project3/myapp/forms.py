from django import forms
from .models import Player


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            "name",
            "nationality",
            "team",
            "national_position",
            "club_position",
            "rating",
            "height",
            "weight",
            "birth_date",
            "age",
            "skill_moves",
            "ball_control",
            "dribbling",
            "speed",
            "strength",
            "player_level",
        ]

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'