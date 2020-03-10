from django.forms import ModelForm
from member.models import Member
from django import forms
from django.utils.translation import gettext as _

class SigninForm(ModelForm): #로그인을 제공하는 class이다.
    class Meta:
        model = Member
        widgets = {'USER_PW':forms.PasswordInput}
        fields = ['USER_ID','USER_PW']       
        labels = {
            'USER_ID': _('사용자 아이디'),
            'USER_PW': _('사용자 비밀번호'),
        } 
    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        self.fields['USER_ID'].initial = ""