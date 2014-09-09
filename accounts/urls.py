from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
        url(r'^login/$', 'account_login', name="login"),
        url(r'^signup/$', 'account_signup', name="signup"),
        url(r'^logout/$', 'account_logout', name="logout"),
    )
