from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.
class Member(models.Model):
    text_validator = MinLengthValidator(12, "길이가 너무 짧습니다.")
    pw_validator = MinLengthValidator(8, "8자 이상이어야 합니다.")
    USER_ID = models.CharField(max_length=20, blank=False, null=False, primary_key=True)
    USER_PW = models.CharField(max_length=100, blank=False, null=False, validators=[pw_validator])
    USER_NAME = models.CharField(max_length=20, blank=False, null=False)
    USER_BIRTH = models.DateTimeField(blank=False, null=False)
    USER_GENDER = models.CharField(max_length=1, blank=False, null=False)
    USER_EMAIL = models.CharField(max_length=50, blank=False, null=False)
    USER_ADDR = models.CharField(max_length=100, blank=False, null=False)
    USER_PH1 = models.CharField(max_length=13, blank=False, null=False, validators=[text_validator])
    USER_PH2 = models.CharField(max_length=13, blank=True, null=True)
    USER_REGIST = models.DateTimeField(blank=False, null=False)
    USER_CK = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        db_table = "member"