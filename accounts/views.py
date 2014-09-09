from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


def account_login(request, template_name='accounts/login.html'):
    """
    Displays the login screen and allows the user to login.
    """
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            return HttpResponseRedirect(reverse("home"))
    context = {
        "form": form
    }
    return render_to_response(template_name, context, RequestContext(request))


def account_signup(request, template_name='accounts/signup.html'):
    """
    Displays a form that allows the users to signup.
    """
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("home"))
    context = {
        "form": form
    }
    return render_to_response(template_name, context, RequestContext(request))
    return render_to_response(template_name, context, RequestContext(request))


def account_logout(request):
    """
    Logout the user.
    """
    logout(request)
    return HttpResponseRedirect(reverse("home"))
