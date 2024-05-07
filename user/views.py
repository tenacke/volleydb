from django.shortcuts import render, redirect
from django.http import HttpResponse

from .utils.forms import UserForm
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

