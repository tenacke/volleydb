from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils.dbmanager import MySQLManager
from django import forms
from django.contrib import messages



from .utils.forms import *
from .utils.usercontroller import UserController

# Create your views here.

def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            controller = UserController()
            if controller.login(form.cleaned_data['username'], form.cleaned_data['password']):
                print(request.session)
                request.session['username'] = controller.username
                request.session['type'] = controller.getType()
                return redirect("home")
            
    else:
        form = UserForm()

    return render(request, 'index.html', {'form': form})


def home(request):
    if 'username' not in request.session:
        return redirect("index")
    return render(request, 'home.html', {'type': request.session['type']})

def add_coach(request):
    manager = MySQLManager()
    if request.method == 'POST':
        form = CoachForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            nationality = form.cleaned_data['nationality']

        manager.add_coach(username, password, name, surname, nationality)
        return render(request, 'home.html',  {'type': request.session['type']})
    else:
        form = CoachForm()

    return render(request, 'add_coach.html', {'form': form})

def add_jury(request):
    manager = MySQLManager()
    if request.method == 'POST':
        form = JuryForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            nationality = form.cleaned_data['nationality']

            manager.add_jury(username, password, name, surname, nationality)
            return render(request, 'home.html',  {'type': request.session['type']})
    else:
        form = JuryForm()

    return render(request, 'add_jury.html', {'form': form})
      

def add_player(request):
    manager = MySQLManager()
    teams = manager.get_teams()
    team_choices = [(team[0], team[1]) for team in teams]
    positions = manager.get_positions()
    position_choices = [(position[0], position[1]) for position in positions]
    
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            dob = form.cleaned_data['dob']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            selected_teams = form.cleaned_data['teams']
            selected_positions = form.cleaned_data['positions']
            
            if not selected_teams or not selected_positions:
                error_message = 'Please select at least one team and one position.'
                return render(request, 'add_player.html', {'form': form, 'team_choices': team_choices, 'position_choices': position_choices, 'error_message': error_message})
            manager.add_player(username, password, name, surname, dob, height, weight, selected_teams, selected_positions)
            return render(request, 'home.html',  {'type': request.session['type']})
    else:
        form = PlayerForm()

    return render(request, 'add_player.html', {'form': form, 'team_choices': team_choices, 'position_choices': position_choices})
