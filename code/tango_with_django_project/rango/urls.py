from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
       url(r'^$', views.index, name='index'),
       url(r'^goto/', views.track_url, name='goto'),
       url(r'^about/', views.about_page, name='about'),
       url(r'^category/(?P<category_id>\w+)/add_page/$', views.add_page, name='add_page'),
       url(r'^category/(?P<category_id>\w+)/[-A-Za-z0-9_]+/$', views.category, name='category'),
       url(r'^add_category/$', views.add_category, name='add_category'),
       url(r'^like_category/$', views.like_category, name='like_category'),
       url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
       url(r'^search/', views.search, name="search"),
       url(r'^register/$', views.register, name='register'),
       url(r'^login/$', views.user_login, name='login'),
       url(r'^profile/$', views.profile, name='profile'),
       url(r'^restricted/$', views.restricted, name='restricted'),
       url(r'^logout/$', views.user_logout, name='logout'),
       )