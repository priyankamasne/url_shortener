from django.conf.urls import patterns, include, url
 
urlpatterns = patterns('mainApp.views',
    url(r'^$', 'index', name='home'),
    url(r'^(?P<short_url>\w{8})$', 'redirect_short_url', name='redirectshorturl'),
    url(r'^encodel/$', 'shorten_url', name='shortenurl'),
)