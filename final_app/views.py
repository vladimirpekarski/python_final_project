from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .models import Players
from django.conf import settings
from . import forms

@login_required(login_url='/login')
def listing(request):
    per_page = settings.USER_PER_PAGE
    form = forms.SearchPlayerForm(request.GET or None)

    if form.is_valid() and form.cleaned_data["email"]:
        email = form.cleaned_data["email"]
        try:
            player = Players.objects.get(email=email)
        except ObjectDoesNotExist:
            player = None

        return render(request, 'final_app/player.html', {'player': player})

    player_list = Players.objects.all()
    paginator = Paginator(player_list, per_page)
    page = request.GET.get('page')
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        players = paginator.page(1)
    except EmptyPage:
        players = paginator.page(paginator.num_pages)

    return render(request, 'final_app/list.html', {'form': form,
                                                   'players': players})


@login_required(login_url='/login')
def change_player_experience(request, player_id):
    player = Players.objects.get(id=player_id)
    form = forms.ChangeExperienceForm(data={"experience": player.xp})

    if request.method == 'POST':
        form = forms.ChangeExperienceForm(request.POST)
        if form.is_valid():
            player.xp = form.cleaned_data["experience"]
            player.save()
            return HttpResponseRedirect("/")

    template_data = {
        "form": form,
        "player": player
    }

    return render(request, 'final_app/change_experience.html/',
                  template_data)

def login_custom(request):
    _next = request.GET.get('next', '/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(_next)
            else:
                HttpResponse('Inactive user.')
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, 'final_app/login.html', {'redirect_to': _next})


def logout_custom(request):
    logout(request)

    return HttpResponseRedirect(settings.LOGIN_URL)
