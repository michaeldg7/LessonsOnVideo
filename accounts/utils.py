import random
import string

from django.contrib.auth.models import User

from annoying.functions import get_object_or_None


def generate_username(username, counter=0):
    """
    Generates a username based on the email address.
    Example: if given email adress is email@example.com, username will be "email" since
    that is the value before "@" in email. If username "email" already exist, the new
    username will be "email1" and so on and so forth in case the username "email" still
    exists.
    """
    new_username = None
    if counter == 0:
        new_username = username
    else:
        new_username = "%s%s" % (username, counter)

    check_username = get_object_or_None(User, username=new_username)

    if check_username is not None:
        return generate_username(username=username, counter=counter+1)
    else:
        return new_username


def generate_random_str(length=64, charset=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    """
    function generates a random for given length and charsetet
    """
    return ''.join(random.choice(charset) for x in range(length))
