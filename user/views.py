from django.shortcuts import render, redirect
from django.db import IntegrityError
from .utils.dbmanager import MySQLManager
from django import forms
from .utils.forms import *
from .utils.usercontroller import UserController

def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            controller = UserController()
            if controller.login(form.cleaned_data['username'], form.cleaned_data['password']):
                request.session['username'] = controller.username
                request.session['type'] = controller.getType()
                return redirect("home")
    else:
        form = UserForm()

    return render(request, 'index.html', {'form': form})

def home(request):
    if 'username' not in request.session:
        return redirect("index")
    return render(request, 'home.html', {'type': request.session['type'], 'username': request.session['username']})

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

            try:
                manager.add_coach(username, password, name, surname, nationality)
            except IntegrityError:
                error_message = "Username already taken, please try another one."
                return render(request, 'add_coach.html', {'form': form, 'error_message': error_message})
            except Exception as e:
                error_message = "Unknown error: {}".format(e)
                return render(request, 'add_coach.html', {'form': form, 'error_message': error_message})
            return redirect("home")
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

            try:
                manager.add_jury(username, password, name, surname, nationality)
            except Exception as e:
                error_message = "Error: {}".format(e)
                return render(request, 'add_jury.html', {'form': form, 'error_message': error_message})
            return redirect("home")
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
            try:
                manager.add_player(username, password, name, surname, dob, height, weight, selected_teams, selected_positions)
            except Exception as e:
                error_message = "Error: {}".format(e)
                return render(request, 'add_player.html', {'form': form, 'team_choices': team_choices, 'position_choices': position_choices, 'error_message': error_message})

            return redirect("home")
    else:
        form = PlayerForm()

    return render(request, 'add_player.html', {'form': form, 'team_choices': team_choices, 'position_choices': position_choices})

def change_stadium_name(request):
    manager = MySQLManager()
    stadiums = manager.get_stadiums()
    stadium_choices = [(stadium[0], stadium[1]) for stadium in stadiums]
    
    if request.method == 'POST':
        form = StadiumForm(request.POST)
        if form.is_valid():
            selected_stadium = form.cleaned_data['stadiums']
            name = form.cleaned_data['name']
            
            if not selected_stadium:
                error_message = 'Please select a stadium.'
                return render(request, 'change_stadium_name.html', {'form': form, 'stadium_choices': stadium_choices})
            try:
                manager.change_stadium_name(selected_stadium, name)
            except Exception as e:
                error_message = "Error: {}".format(e)
                return render(request, 'change_stadium_name.html', {'form': form, 'stadium_choices': stadium_choices, 'error_message': error_message})

            return redirect("home")
    else:
        form = StadiumForm()

    return render(request, 'change_stadium_name.html', {'form': form, 'stadium_choices': stadium_choices})

def ratings(request):
    manager = MySQLManager()
    average_ratings = -1
    count_ratings = -1
    try:
        average_ratings = manager.average_ratings(request.session['username'])
        count_ratings = manager.count_ratings(request.session['username'])
    except Exception as e:
        error_message = "Error: {}".format(e)
        return render(request, 'jury_ratings.html', {'average_ratings':average_ratings, 'count_ratings':count_ratings })
    return render(request, 'jury_ratings.html', {'average_ratings':average_ratings, 'count_ratings':count_ratings })
