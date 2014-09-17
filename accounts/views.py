from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

from accounts.forms import CustomUserCreationForm, LoginForm
from accounts.models import RegistrationToken
from accounts.utils import generate_random_str

from annoying.functions import get_object_or_None


def account_login(request, template_name='accounts/login.html'):
    """
    Displays the login screen and allows the user to login.
    """
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            auth_user = get_object_or_None(User, email=email)
            if auth_user:
                user = authenticate(username=auth_user.username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        next = request.GET.get("next", None)
                        if next:
                            return HttpResponseRedirect(next)
                        return HttpResponseRedirect(reverse('home'))
    context = {
        "form": form
    }
    return render_to_response(template_name, context, RequestContext(request))


def account_signup(request, template_name='accounts/signup.html'):
    """
    Displays a form that allows the users to signup.
    """
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            # if user is not None:
            #     if user.is_active:
            #         login(request, user)
            #         return HttpResponseRedirect(reverse("home"))
            token = generate_random_str()
            reg_token = RegistrationToken.objects.create(user=new_user, token=token)

            headers = {"From": "LessonsOnVideo"}
            subject = "LessonsOnVideo Registration Activation"
            sender = settings.EMAIL_FROM
            cont = {
                'user': new_user.email,
                'host': "http://%s" % request.get_host(),
                'link': reverse('registration-complete', args=(new_user.username, token))
            }
            email_content = render_to_string("accounts/email/activation_email.txt", cont)

            # send registration email
            #send_mail(subject, email_content, sender, [new_user.email], fail_silently=False)
            msg = EmailMessage(subject, email_content, sender, [new_user.email], headers=headers)
            msg.send()
            return HttpResponseRedirect(reverse('registration-confirm'))
    context = {
        "form": form
    }
    return render_to_response(template_name, context, RequestContext(request))


def account_logout(request):
    """
    Logout the user.
    """
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def registration_confirm(request):
    """
    Displays a message to activate the user's email

    **Context**
    ``RequestContext``

    **Template:**
    :template:`accounts/registration_confirm.html`

    """
    return render_to_response('accounts/registration_confirm.html', {}, RequestContext(request))


def registration_complete(request, username, token):
    """
    Validates the token used in activating a user

    **Context**
    ``RequestContext``

    ``accounts``
        An instance of :model:`accounts.RegistrationToken`
    ``user``
        An instance of :model:`auth.user`

    ***Template:***
    :template:`accounts/registration_complete.html`

    """
    context = {}
    new_user = get_object_or_None(User, username=username)
    check_token = get_object_or_None(RegistrationToken, user=new_user, token=token)
    success = False

    if check_token and new_user:
        new_user.is_active = True
        new_user.save()
        # delete all tokens after activation
        RegistrationToken.objects.filter(user=new_user).delete()
        success = True
    context["success"] = success
    return render_to_response("accounts/registration_complete.html", context, RequestContext(request))
