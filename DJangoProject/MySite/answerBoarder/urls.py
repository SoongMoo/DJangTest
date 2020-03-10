from django.conf.urls import url
from . import views

app_name = 'answerBoarder'
urlpatterns = [
    url('BoardReplyAction', views.BoardReplyAction),
    url('BoardModifyAction', views.BoardModifyAction),
    url('answerBoardWritePro', views.answerBoardWritePro),    
    url('answerBoardList', views.answerBoardList),
    url('answerBoard', views.answerBoard),
    url('AnswerBoarderDetail/(?P<BOARD_NUM>\w+)/$', views.AnswerBoarderDetail),
    url('BoardModify', views.BoardModify),
    url('BoardReply', views.BoardReply),
    
]
