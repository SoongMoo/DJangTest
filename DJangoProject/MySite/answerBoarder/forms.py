from django.forms import ModelForm
from .models import AnswerBoarder
from django import forms
from django.utils.translation import gettext as _

class BoardWriteForm(ModelForm): 
    BOARD_ORIGINAL_FILENAME = forms.FileField(label = '등록 할 파일', required=False,widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model=AnswerBoarder
        widgets = {'BOARD_PASS':forms.PasswordInput,'BOARD_CONTENT':forms.Textarea}
        fields = ['BOARD_NAME','BOARD_PASS','BOARD_SUBJECT','BOARD_CONTENT','BOARD_ORIGINAL_FILENAME']
        labels = {
            'BOARD_NAME': _('글쓴이'),
            'BOARD_PASS': _('비밀번호'),
            'BOARD_SUBJECT': _('글 제목'),
            'BOARD_CONTENT': _('글 내용'),
        }
        
class BoardInfoForm(ModelForm):
    class Meta:
        model=AnswerBoarder
        widgets = {'BOARD_PASS':forms.PasswordInput,'BOARD_CONTENT':forms.Textarea}
        fields = ['BOARD_NAME','BOARD_PASS','BOARD_SUBJECT','BOARD_CONTENT']
        labels = {
            'BOARD_NAME': _('글쓴이'),
            'BOARD_PASS': _('비밀번호'),
            'BOARD_SUBJECT': _('글 제목'),
            'BOARD_CONTENT': _('글 내용'),
        }
        def __init__(self, *args, **kwargs):
            super(BoardInfoForm, self).__init__(*args, **kwargs)