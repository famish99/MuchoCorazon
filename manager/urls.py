from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import game.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'', include('social_auth.urls')),
    url(r'^$', game.views.HomeView.as_view()),
    url(r'^games/$', game.views.GameList.as_view()),
    url(r'^logout/$', game.views.logout_view),
    # url(r'^$', 'tanto.views.home', name='home'),
    # url(r'^tanto/', include('tanto.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
