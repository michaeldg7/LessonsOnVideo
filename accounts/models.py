from django.contrib.auth.models import User
from django.db import models


class RegistrationToken(models.Model):
    """
    Stores a token to be used to verify an email address in registration related to :model: `auth.User`
    """
    user = models.ForeignKey(User)
    token = models.CharField(max_length=100)

    def __unicode__(self):
        return "%r" % self.user.username

    class Meta:
        verbose_name = "Registration Token"
        verbose_name_plural = "Registration Tokens"
