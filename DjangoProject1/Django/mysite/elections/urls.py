from django.conf.urls import url
from . import views
app_name = 'elections'
urlpatterns = [
	url(r'^$', views.index, name = 'home'),
	url(r'^areas/(?P<area>[가-힣]+)/$', views.areas),  #①
	url(r'^areas/(?P<area>[가-힣]+)/results$', views.results), #②  
	url(r'^polls/(?P<poll_id>\d+)/$', views.polls), #③
	url(r'^candidates/(?P<name>[가-힣]+)/$', views.candidates)
]
