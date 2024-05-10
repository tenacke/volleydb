from django.shortcuts import render, redirect
from django.db import IntegrityError
from .utils.dbmanager import MySQLManager
from .utils.forms import *
from .utils.usercontroller import UserController


def index(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            controller = UserController()
            if controller.login(
                form.cleaned_data["username"], form.cleaned_data["password"]
            ):
                request.session["username"] = controller.username
                request.session["type"] = controller.type
                return redirect("home")
            else:
                return render(
                    request,
                    "index.html",
                    {
                        "form": form,
                        "error_message": "Wrong username and/or password. Please try again.",
                    },
                )
    else:
        form = UserForm()

    return render(request, "index.html", {"form": form})


def home(request):
    if "username" not in request.session:
        return redirect("index")
    return render(
        request,
        "home.html",
        {"type": request.session["type"], "username": request.session["username"]},
    )


def add_coach(request):
    manager = MySQLManager()
    if request.method == "POST":
        form = CoachForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            name = form.cleaned_data["name"]
            surname = form.cleaned_data["surname"]
            nationality = form.cleaned_data["nationality"]

            try:
                manager.add_coach(username, password, name, surname, nationality)
            except IntegrityError:
                error_message = "Username already taken, please try another one."
                return render(
                    request,
                    "add_coach.html",
                    {"form": form, "error_message": error_message},
                )
            except Exception as e:
                error_message = "Unknown error: {}".format(e)
                return render(
                    request,
                    "add_coach.html",
                    {"form": form, "error_message": error_message},
                )
            return redirect("home")
    else:
        form = CoachForm()

    return render(request, "add_coach.html", {"form": form})


def add_jury(request):
    manager = MySQLManager()
    if request.method == "POST":
        form = JuryForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            name = form.cleaned_data["name"]
            surname = form.cleaned_data["surname"]
            nationality = form.cleaned_data["nationality"]

            try:
                manager.add_jury(username, password, name, surname, nationality)
            except Exception as e:
                error_message = "Error: {}".format(e)
                return render(
                    request,
                    "add_jury.html",
                    {"form": form, "error_message": error_message},
                )
            return redirect("home")
    else:
        form = JuryForm()

    return render(request, "add_jury.html", {"form": form})


def add_player(request):
    manager = MySQLManager()
    teams = manager.get_teams()
    team_choices = [(team[0], team[1]) for team in teams]
    positions = manager.get_positions()
    position_choices = [(position[0], position[1]) for position in positions]

    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            name = form.cleaned_data["name"]
            surname = form.cleaned_data["surname"]
            dob = form.cleaned_data["dob"]
            height = form.cleaned_data["height"]
            weight = form.cleaned_data["weight"]
            selected_teams = form.cleaned_data["teams"]
            selected_positions = form.cleaned_data["positions"]

            if not selected_teams or not selected_positions:
                error_message = "Please select at least one team and one position."
                return render(
                    request,
                    "add_player.html",
                    {
                        "form": form,
                        "team_choices": team_choices,
                        "position_choices": position_choices,
                        "error_message": error_message,
                    },
                )
            try:
                manager.add_player(
                    username,
                    password,
                    name,
                    surname,
                    dob,
                    height,
                    weight,
                    selected_teams,
                    selected_positions,
                )
            except Exception as e:
                error_message = "Error: {}".format(e)
                return render(
                    request,
                    "add_player.html",
                    {
                        "form": form,
                        "team_choices": team_choices,
                        "position_choices": position_choices,
                        "error_message": error_message,
                    },
                )

            return redirect("home")
    else:
        form = PlayerForm()

    return render(
        request,
        "add_player.html",
        {
            "form": form,
            "team_choices": team_choices,
            "position_choices": position_choices,
        },
    )


def change_stadium_name(request):
    manager = MySQLManager()
    stadiums = manager.get_stadiums()
    stadium_choices = [(stadium[0], stadium[1]) for stadium in stadiums]

    if request.method == "POST":
        form = StadiumForm(request.POST)
        if form.is_valid():
            selected_stadium = form.cleaned_data["stadiums"]
            name = form.cleaned_data["name"]

            if not selected_stadium:
                error_message = "Please select a stadium."
                return render(
                    request,
                    "change_stadium_name.html",
                    {"form": form, "stadium_choices": stadium_choices},
                )
            try:
                manager.change_stadium_name(selected_stadium, name)
            except Exception as e:
                error_message = "Error: {}".format(e)
                return render(
                    request,
                    "change_stadium_name.html",
                    {
                        "form": form,
                        "stadium_choices": stadium_choices,
                        "error_message": error_message,
                    },
                )

            return redirect("home")
    else:
        form = StadiumForm()

    return render(
        request,
        "change_stadium_name.html",
        {"form": form, "stadium_choices": stadium_choices},
    )


def ratings(request):
    manager = MySQLManager()
    average_ratings = -1
    count_ratings = -1
    try:
        average_ratings = manager.average_ratings(request.session["username"])
        count_ratings = manager.count_ratings(request.session["username"])
    except Exception as e:
        error_message = "Error: {}".format(e)
        return render(
            request,
            "jury_ratings.html",
            {"average_ratings": average_ratings, "count_ratings": count_ratings},
        )
    return render(
        request,
        "jury_ratings.html",
        {"average_ratings": average_ratings, "count_ratings": count_ratings},
    )


def add_match_session(request):
    manager = MySQLManager()
    # stadiums = manager.get_stadiums()
    # stadium_choices = [(stadium[0], stadium[1]) for stadium in stadiums]
    # time_slots = [1, 2, 3, 4]

    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            stadium = form.cleaned_data["stadium"]
            date = form.cleaned_data["date"]
            time_slot = form.cleaned_data["time_slot"]
            jury = form.cleaned_data["jury"]

            try:
                team = manager.get_team_by_coach_username(
                    request.session["username"], date
                )
                print(date, team)
                if team is None:
                    error_message = "You have no team for this date."
                    return render(
                        request,
                        "add_match_session.html",
                        {"form": form, "error_message": error_message},
                    )
                manager.add_match_session(stadium, date, time_slot, jury, team[0])
            except Exception as e:
                error_message = "Error: {}".format(e)
                return render(
                    request,
                    "add_match_session.html",
                    {"form": form, "error_message": error_message},
                )

            return redirect("home")
    else:
        form = SessionForm()

    return render(request, "add_match_session.html", {"form": form})


def delete_match_session(request):
    manager = MySQLManager()
    sessions = manager.get_sessions_by_coach_username(
        request.session["username"], False
    )
    if request.method == "POST":
        form = DeleteSessionForm(request.POST, sessions=sessions)
        if form.is_valid():
            session_id = form.cleaned_data["session_id"]
            try:
                manager.delete_match_session(session_id)
            except Exception as e:
                error_message = "Error: {}".format(e)
                return render(
                    request,
                    "delete_match_session.html",
                    {"form": form, "error_message": error_message},
                )

            return redirect("home")
    else:
        form = DeleteSessionForm(sessions=sessions)

    return render(request, "delete_match_session.html", {"form": form})


def list_stadiums(request):
    manager = MySQLManager()
    stadiums = [
        {"name": stadium[1], "country": stadium[2]}
        for stadium in manager.get_stadiums()
    ]
    return render(request, "list_stadiums.html", {"stadiums": stadiums})


def add_squad(request):
    manager = MySQLManager()
    sessions = manager.get_sessions_by_coach_username(request.session["username"], True)
    if not sessions:
        error_message = "You have no available sessions."
        return render(request, "add_squad.html", {"error_message": error_message})
    if request.method == "POST":
        form = SessionSquadForm(
            request.POST,
            sessions=sessions,
        )
        if form.is_valid():
            session_id = form.cleaned_data["session_id"]
            request.session["session_id"] = session_id
            return redirect("add_squad_player")
    else:
        form = SessionSquadForm(sessions=sessions)

    return render(request, "add_squad.html", {"form": form})


def add_squad_player(request):
    manager = MySQLManager()
    session_id = request.session["session_id"]
    players = manager.get_players_by_session_id(session_id)
    if request.method == "POST":
        form = AddSquadForm(request.POST, players=players)
        if form.is_valid():
            selected_players = form.cleaned_data["players"]
            request.session["selected_players"] = [
                (player[0], f"{player[1]} {player[2]}")
                for player in players
                if player[0] in selected_players
            ]
            return redirect("add_squad_position")
    else:
        form = AddSquadForm(players=players)

    return render(request, "add_squad_player.html", {"form": form})


def add_squad_position(request):
    selected_players = request.session["selected_players"]
    if request.method == "POST":
        form = AddSquadPositionForm(request.POST, players=selected_players)
        if form.is_valid():
            positions = []
            for player in selected_players:
                position = form.cleaned_data[f"position_{player[0]}"]
                positions.append((player[0], position))
            manager = MySQLManager()
            try:
                manager.add_squad(request.session["session_id"], positions)
            except Exception as e:
                error_message = "Error: {}".format(e)
                manager.delete_squad(request.session["session_id"])
                return render(
                    request,
                    "add_squad_position.html",
                    {"form": form, "error_message": error_message},
                )

            return redirect("home")
    else:
        form = AddSquadPositionForm(players=selected_players)

    return render(request, "add_squad_position.html", {"form": form})


def rate_match(request):
    manager = MySQLManager()
    matches = manager.get_rating_matches(request.session["username"])
    match_choices = [(match[0], match[1]) for match in matches]
    if len(matches) == 0:
        error_message = "No matches for you to rate"
        return render(
            request,
            "home.html",
            {
                "type": request.session["type"],
                "username": request.session["username"],
                "error_message": error_message,
            },
        )

    if request.method == "POST":
        form = RateMatchForm(request.POST, username=request.session["username"])
        if form.is_valid():
            selected_match = form.cleaned_data["matches"]
            rating = form.cleaned_data["rating"]

            if not selected_match:
                error_message = "Please select a match you want to rate."
                return render(
                    request,
                    "rate_match.html",
                    {"form": form, "match_choices": match_choices},
                )
            try:
                manager.rate_match(selected_match, rating)
            except Exception as e:
                error_message = "Error: {}".format(e)
                return render(
                    request,
                    "rate_match.html",
                    {
                        "form": form,
                        "match_choices": match_choices,
                        "error_message": error_message,
                    },
                )

            return redirect("home")
    else:
        form = RateMatchForm(username=request.session["username"])

    return render(
        request,
        "rate_match.html",
        {"form": form, "match_choices": match_choices},
    )


def player(request):
    manager = MySQLManager()
    played_with = []
    try:
        played_with = manager.players(request.session["username"])
        height = manager.players_height(request.session["username"])
    except Exception as e:
        error_message = "Error: {}".format(e)
        return render(
            request,
            "player.html",
            {"players": played_with, "height": height, "error_message": error_message},
        )
    return render(
        request,
        "player.html",
        {"players": played_with, "height": height},
    )
