from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, "basic_app/index.html")


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)  # hashes password automatically
            user.save()

            # Saving with commit=False gets you a model object, then you can add your extra data and save it.
            # Dont commit yet as may get erros because of collisions if it tries to overwrite user
            # we will save avter we instantiate profile.user
            profile = profile_form.save(commit=False)
            #  note in models.py: user = models.OneToOneField(User)
            profile.user = user
            # check if user uploaded pic
            if "profile_pic" in request.FILES:
                profile.profile_pic = request.FILES["profile_pic"]

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, "basic_app/register.html",
                {"user_form": user_form,
                "profile_form": profile_form,
                "registered": registered})

@login_required
def special(request):
    return HttpResponse("You're logged in, awesome!")


@login_required
def user_logout(request):
    # logout of current session
    '''
    What is a session?

    Django provides full support for anonymous sessions. The session framework
    lets you store and retrieve arbitrary data on a per-site-visitor basis.
    It stores data on the server side and abstracts the sending and receiving of
    cookies. Cookies contain a session ID – not the data itself (unless you’re
    using the cookie based backend).
    '''
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def user_login(request):
    if request.method == "POST":
        # From name in login.html: <input type="text" name="username" placeholder="Username">
        username = request.POST.get("username")
        password = request.POST.get("password")

        # authenticate Tries to authenticate username with password by calling User.check_password.
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                '''
                HttpResponseRedirect is meant to send a 3xx HTTP code and
                redirect to another URL (that is, the response is a redirect header).
                It is actually a subclass of HttpResponse, and can be used as a
                shortcut for redirects.

                HttpResponse, on the other hand is the main response object,
                where you can set headers / body, etc (and is what you usually
                 use for sending a rendered template and so on
                '''
                login(request, user)
                # reverse given rendered url for a given view name
                # e.g. this will return r"&" as 127.0.0.1:8000
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, "basic_app/login.html", {})
