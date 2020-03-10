from django.db import models

# Create your models here.
from member.models import Member
# Create your models here.
from django.core.validators import MinLengthValidator

from datetime import datetime
from django.conf import settings

import os
# Create your models here.

class AnswerBoarder(models.Model):
    def __str__(self):
        return self.BOARD_NUM
    pw_validator = MinLengthValidator(8, "8자 이상이어야 합니다.")
    BOARD_NUM = models.BigAutoField(blank=False, null=False, primary_key=True)
    USER_ID = models.ForeignKey(Member, on_delete=models.CASCADE)
    BOARD_NAME = models.CharField(max_length=20, blank=False, null=False)
    BOARD_PASS = models.CharField(max_length=200, blank=False, null=False, validators=[pw_validator])
    BOARD_SUBJECT = models.CharField(max_length=50, blank=False, null=False)
    BOARD_CONTENT = models.CharField(max_length=2000, blank=True, null=True)
    BOARD_RE_REF = models.DecimalField(max_digits = 6, decimal_places = 0,blank=False, null=False, default = 0)
    BOARD_RE_LEV = models.DecimalField(max_digits = 6, decimal_places = 0,blank=False, null=False, default = 0)
    BOARD_RE_SEQ = models.DecimalField(max_digits = 6, decimal_places = 0,blank=False, null=False, default = 0)
    BOARD_READCOUNT = models.DecimalField(max_digits = 6, decimal_places = 0,blank=False, null=False, default = 0)
    BOARD_DATE = models.DateTimeField(blank=False, null=False, default=datetime.now)
    BOARD_ORIGINAL_FILENAME = models.CharField(max_length=500, blank=True, null=True)
    BOARD_STORE_FILENAME = models.CharField(max_length=500, blank=True, null=True)
    BOARD_FILE_SIZE = models.CharField(max_length=200, blank=True, null=True)
    
    def delete(self, *args, **kargs):
        fileNames = self.BOARD_STORE_FILENAME.split("`")
        for index, value in enumerate(fileNames):
            print(value)
            if value != "":
                os.remove(os.path.join(settings.MEDIA_ROOT+"\\uploads\\",value))
        super(AnswerBoarder, self).delete(*args, **kargs)

    class Meta:
        db_table = "ANSWERBOARDER"
        
