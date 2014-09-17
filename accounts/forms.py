from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from annoying.functions import get_object_or_None

from accounts.utils import generate_username


class CustomUserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    email = forms.CharField(label='Email', required=True)
    email2 = forms.CharField(label='Confirm Email', required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = "form-control"

    def clean_email2(self):
        email1 = self.cleaned_data.get("email") or ""
        email2 = self.cleaned_data.get("email2") or ""
        if (email1 or email2)and email1 != email2:
            raise forms.ValidationError("Emails don't match")
        elif (email1 or email2)and email1 == email2:
            if User.objects.filter(email=email2).exists():
                raise forms.ValidationError("Email address is already used. Please provided a different email address")
        return email2

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(CustomUserCreationForm, self).save(commit=False)
        email = self.cleaned_data["email"].split("@")
        user.username = slugify(generate_username(username=email[0]))
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """
    User authentication form
    """
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = "form-control"

    def clean(self):
        """
        Validates data
        """
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = get_object_or_None(User, email=email)
            if user:
                self.user_cache = authenticate(username=user.username, password=password)
                if self.user_cache is None:
                    raise forms.ValidationError(_("Please enter a correct email and password. Note that both fields are case-sensitive."))
                elif not self.user_cache.is_active:
                    raise forms.ValidationError(_("This account is inactive."))

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("The email you have entered does not exist.")
        return email

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
