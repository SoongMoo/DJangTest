from django.conf.urls import url
from . import views

app_name = 'Main'
urlpatterns = [
    url(r'^$', views.index),
    url('logout', views.logout),
    url('loginAction', views.loginAction),
]