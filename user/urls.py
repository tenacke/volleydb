from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("add_player", views.add_player, name="add_player"),
    path("add_coach", views.add_coach, name="add_coach"),
    path("add_jury", views.add_jury, name="add_jury"),
    path("change_stadium_name", views.change_stadium_name, name="change_stadium_name"),
    path("jury_ratings", views.ratings, name="ratings"),
    path("add_match_session", views.add_match_session, name="add_match_session"),
    path(
        "delete_match_session", views.delete_match_session, name="delete_match_session"
    ),
    path("list_stadiums", views.list_stadiums, name="list_stadiums"),
    path("add_squad", views.add_squad, name="add_squad"),
    path("rate_match", views.rate_match, name= "rate_match"),
    path("player", views.player, name = "player")
]
