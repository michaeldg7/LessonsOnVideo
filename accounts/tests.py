import re

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core import mail

from django_webtest import WebTest
from django_dynamic_fixture import G


class AccountTest(WebTest):
    user_name = 'test_user'
    email = 'test_user@example.com'
    password = 'password'

    def setUp(self):
        super(AccountTest, self).setUp()
        self.test_user = G(User, username=self.user_name, email=self.email)
        self.test_user.set_password(self.password)
        self.test_user.save()

    def test_wrong_password_signin(self):
        response = self.app.get(reverse('login'), status=200)
        
        form = response.forms["login-form"]
        form['email'] = self.email
        form['password'] = 'TheWrongPassword'

        response = form.submit()

        self.assertContains(
            response,
            'Please enter a correct email and password. Note that both fields are case-sensitive.',
            status_code=200
        )

    def test_wrong_email_signin(self):
        response = self.app.get(reverse('login'), status=200)

        form = response.forms["login-form"]
        form['email'] = 'TheWrongEmail@example.pl'
        form['password'] = self.password

        response = form.submit()

        self.assertContains(
            response,
            'The email you have entered does not exist.',
            status_code=200
        )

    def test_signin(self):
        response = self.app.get(reverse('login'), status=200)

        form = response.forms["login-form"]
        form['email'] = self.email
        form['password'] = self.password

        response = form.submit()

        self.assertRedirects(response, reverse('home'))

    def test_signup(self):
        response = self.app.get(reverse('signup'), status=200)

        form = response.forms["signup-form"]
        form['email'] = 'signup_test_user@example.pl'
        form['email2'] = 'signup_test_user@example.pl'
        form['password1'] = self.password
        form['password2'] = self.password

        response = form.submit()

        self.assertRedirects(response, reverse('registration-confirm'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, 'LessonsOnVideo Registration Activation'
        )

        response = self.app.get(re.search('http(.*?)\n',
                                mail.outbox[0].body).group(0), status=200)

        self.assertContains(
            response,
            'You have successfully activated your account.',
            status_code=200
        )