from django.contrib import admin

from accounts.models import RegistrationToken


class RegistrationTokenAdmin(admin.ModelAdmin):
    """
    Admin view for :model:'accounts.RegistrationToken' model
    """
    model = RegistrationToken


admin.site.register(RegistrationToken, RegistrationTokenAdmin)
