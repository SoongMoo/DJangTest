from django.conf.urls import url
from . import views

app_name = 'member'
urlpatterns = [
    url('memberPasswordModifyPro', views.memberPasswordModifyPro),
    url('memberModifyPro', views.memberModifyPro),
    url('memberDelete', views.memberDelete),
      
    url('agree', views.agree),
    url('regist', views.regist),
    url('memberJoinAction', views.memberJoinAction),
    url('memberDetail', views.memberDetail),
    url('memberMail/(?P<USER_CK>\w+)/$', views.memberMail), 
    
    url('memberModify', views.memberModify),
    url('changePassword', views.changePassword),
    url('memberPasswordPro', views.memberPasswordPro),
    
    url('memberlist', views.memberlist),
    url('memberInfo/(?P<USER_ID>\w+)/$', views.memberInfo),   
]