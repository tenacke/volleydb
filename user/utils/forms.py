from django import forms
from .dbmanager import MySQLManager


class UserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", max_length=100)


class CoachForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, required=True)
    password = forms.CharField(label="Password", max_length=100, required=False)
    name = forms.CharField(label="Name", required=False)
    surname = forms.CharField(label="Surname", required=False)
    nationality = forms.CharField(label="Nationality", required=True)


class JuryForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, required=True)
    password = forms.CharField(label="Password", max_length=100, required=False)
    name = forms.CharField(label="Name", required=False)
    surname = forms.CharField(label="Surname", required=False)
    nationality = forms.CharField(label="Nationality", required=True)


class PlayerForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput, required=False
    )
    name = forms.CharField(label="Name", required=False)
    surname = forms.CharField(label="Surname", required=False)
    dob = forms.DateField(
        label="Date of Birth (DD.MM.YYYY)", required=False, input_formats=["%d.%m.%Y"]
    )
    height = forms.DecimalField(label="Height", required=False)
    weight = forms.DecimalField(label="Weight", required=False)
    teams = forms.MultipleChoiceField(
        label="Teams (team_id, team_name)",
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    positions = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        manager = MySQLManager()
        teams = manager.get_teams()
        self.fields["teams"].choices = [
            (team[0], f"({team[0]}, {team[1]})") for team in teams
        ]
        positions = manager.get_positions()
        self.fields["positions"].choices = [
            (position[0], position[1]) for position in positions
        ]

    def clean(self):
        cleaned_data = super(PlayerForm, self).clean()
        teams = cleaned_data.get("teams")
        positions = cleaned_data.get("positions")
        if not teams or not positions:
            raise forms.ValidationError(
                "Please select at least one team and one position."
            )
        return cleaned_data


class StadiumForm(forms.Form):
    stadiums = forms.ChoiceField(widget=forms.RadioSelect)
    name = forms.CharField(label="New Stadium Name", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        manager = MySQLManager()
        stadiums = manager.get_stadiums()
        self.fields["stadiums"].choices = [
            (stadium[0], stadium[1]) for stadium in stadiums
        ]

    def clean(self):
        cleaned_data = super().clean()
        stadiums = cleaned_data.get("stadiums")

        if not stadiums:
            raise forms.ValidationError("Please select a stadium.")

        return cleaned_data


class SessionForm(forms.Form):
    stadium = forms.ChoiceField(label="Stadium", widget=forms.Select)
    date = forms.DateField(label="Date (DD.MM.YYYY)", input_formats=["%d.%m.%Y"])
    time_slot = forms.ChoiceField(label="Time Slot", widget=forms.Select)
    jury = forms.ChoiceField(label="Jury", widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        manager = MySQLManager()
        stadiums = manager.get_stadiums()
        self.fields["stadium"].choices = [
            (stadium[0], stadium[1]) for stadium in stadiums
        ]
        self.fields["time_slot"].choices = [(1, 1), (2, 2), (3, 3), (4, 4)]
        juries = manager.get_juries()
        self.fields["jury"].choices = [
            (jury[0], f"{jury[1]} {jury[2]}") for jury in juries
        ]

    def clean(self):
        cleaned_data = super().clean()
        stadium = cleaned_data.get("stadium")
        date = cleaned_data.get("date")
        time_slot = cleaned_data.get("time_slot")
        jury = cleaned_data.get("jury")

        if not stadium or not date or not time_slot or not jury:
            raise forms.ValidationError("Please fill all fields.")

        return cleaned_data


class DeleteSessionForm(forms.Form):
    session_id = forms.IntegerField(label="Session ID", required=True)


class SessionSquadForm(forms.Form):
    session_id = forms.ChoiceField(label="Session ID", widget=forms.Select)

    def __init__(self, *args, **kwargs):
        sessions = kwargs.pop("sessions")
        super().__init__(*args, **kwargs)
        self.fields["session_id"].choices = [
            (session[0], session[0]) for session in sessions
        ]


class AddSquadForm(forms.Form):
    players = forms.MultipleChoiceField(
        label="Players",
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["players"].choices = kwargs["players"]

    def clean(self):
        cleaned_data = super().clean()
        players = cleaned_data.get("players")

        if not players:
            raise forms.ValidationError("Please fill all fields.")

        if len(players) != 6:
            raise forms.ValidationError("Please select 6 players.")

        return cleaned_data
