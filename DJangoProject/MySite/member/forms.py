from django.forms import ModelForm
from .models import Member
from django import forms
from django.utils.translation import gettext as _

class SignupForm(ModelForm): #회원가입을 제공하는 class이다.
    USER_GENDER_CHOICES = [('M', '남자'),('F', '여자'),]
    USER_PW_Con = forms.CharField(max_length=200, widget=forms.PasswordInput(),label = '사용자 비밀번호 확인',help_text = '입력한 사용자 비밀번호와 같아야 합니다.')
    USER_GENDER = forms.ChoiceField(choices=USER_GENDER_CHOICES, widget=forms.RadioSelect, label = '성별', initial='M')
    USER_EMAIL = forms.EmailField(label = '사용자 이메일')

    class Meta:
        model=Member
        widgets = {'USER_PW':forms.PasswordInput}
        fields = ['USER_ID','USER_PW','USER_PW_Con','USER_NAME','USER_BIRTH','USER_GENDER','USER_EMAIL','USER_ADDR', 'USER_PH1', 'USER_PH2']

        help_texts = {
            'USER_BIRTH': _('yyyy-MM-dd 형식으로 입력해주세요'),
        }
        labels = {
            'USER_ID': _('사용자 아이디'),
            'USER_PW': _('사용자 비밀번호'),
            'USER_NAME': _('사용자 이름'),
            'USER_BIRTH': _('사용자 생년월일'),
            'USER_ADDR': _('사용자 주소'),
            'USER_PH1': _('사용자  연락처1'),
            'USER_PH2': _('사용자 연락처2'),
        } 
    
