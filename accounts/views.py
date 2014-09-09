from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


# Create your views here.
def account_logout(request):
    """
    Logout the user.
    """
    logout(request)
    return HttpResponseRedirect(reverse("home"))
