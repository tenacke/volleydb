from django import forms
from .dbmanager import MySQLManager


class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)

class PlayerForm(forms.Form):
    username = forms.CharField(label='Username', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    name = forms.CharField(label='Name', required=False)
    surname = forms.CharField(label='Surname', required=False)
    dob = forms.DateField(label='Date of Birth', required=False)
    height = forms.DecimalField(label='Height', required=False)
    weight = forms.DecimalField(label='Weight', required=False)
    teams = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=True)
    positions = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        manager = MySQLManager()
        teams = manager.get_teams()
        self.fields['teams'].choices = [(team[0], team[1]) for team in teams]
        positions = manager.get_positions()
        self.fields['positions'].choices = [(position[0], position[1]) for position in positions]
    def clean(self):
        cleaned_data = super(PlayerForm, self).clean()
        teams = cleaned_data.get('teams')
        positions = cleaned_data.get('positions')
        if not teams or not positions:
            raise forms.ValidationError("Please select at least one team and one position.")
        return cleaned_data
