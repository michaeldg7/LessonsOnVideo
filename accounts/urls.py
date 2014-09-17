from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
        url(r'^login/$', 'account_login', name="login"),
        url(r'^signup/$', 'account_signup', name="signup"),
        url(r'^logout/$', 'account_logout', name="logout"),
        url(r"^confirm/$", "registration_confirm", name="registration-confirm"),
        url(r"^activate/(?P<username>.*)/(?P<token>.*)/$", "registration_complete",
        name="registration-complete"),
    )
