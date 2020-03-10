from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .forms import BoardWriteForm
from .models import AnswerBoarder


from django.core.paginator import Paginator
import math
def answerBoardList(request):
    answerBoarder = AnswerBoarder.objects.all().order_by('-BOARD_RE_REF','BOARD_RE_SEQ')
    page = request.GET.get('page',1)
    limit = 10
    page_range = 10
    paginator = Paginator(answerBoarder, limit)
    contacts = paginator.get_page(page)
    
    current_block = math.ceil(int(page)/page_range)
    start_block = (current_block-1) * page_range
    end_block = start_block + page_range
    p_range = paginator.page_range[start_block:end_block]
    
    
    context = {'contacts': contacts,'p_range' : p_range,}
    return render(request, 'answerBoarder/Board_List.html',context)

def answerBoard(request):
    return render(request, 'answerBoarder/Board_Write.html',{'f':BoardWriteForm()})

import os
from member.models import Member
from member.views import pwEncypt
from django.core.files.storage import FileSystemStorage
from django.db.models import Max 

import uuid
@csrf_exempt
def answerBoardWritePro(request):
    member  = Member.objects.get(USER_ID=request.session['member']['USER_ID'])
    boarderNum = AnswerBoarder.objects.aggregate(BOARD_NUM=Max('BOARD_NUM'))
    if boarderNum['BOARD_NUM'] is None:
        boarderNum['BOARD_NUM'] = 1
    else :
        boarderNum['BOARD_NUM'] += 1
    print(boarderNum['BOARD_NUM'])
    form = BoardWriteForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            answerBoarder = AnswerBoarder()
            fs = FileSystemStorage('../static/media/uploads/')
            myfiles = request.FILES.getlist('BOARD_ORIGINAL_FILENAME')
            fileNames = ""
            fileSize = ""
            originalName=""
            for myfile in myfiles:
                file = fs.save(myfile.name, myfile)
                fileSize += str(os.path.getsize("../static/media/uploads/" + file)) + "`"
                extension = file.rsplit('.', 1)[1]
                fileName = uuid.uuid4().__str__().replace('-', '')
                os.rename('../static/media/uploads/' + file , '../static/media/uploads/' + fileName +"." + extension)
                originalName += file + "`"
                fileNames += fileName +"." + extension+ "`"
            answerBoarder.BOARD_NUM = boarderNum['BOARD_NUM']
            answerBoarder.BOARD_ORIGINAL_FILENAME = originalName
            answerBoarder.BOARD_STORE_FILENAME = fileNames
            answerBoarder.BOARD_FILE_SIZE = fileSize
            answerBoarder.BOARD_NAME = request.POST['BOARD_NAME']
            answerBoarder.BOARD_PASS = pwEncypt(request.POST['BOARD_PASS'])
            answerBoarder.BOARD_SUBJECT = request.POST['BOARD_SUBJECT']
            answerBoarder.BOARD_CONTENT = request.POST['BOARD_CONTENT']
            answerBoarder.BOARD_RE_REF = boarderNum['BOARD_NUM']
            answerBoarder.USER_ID = member # 외래키로 지정된 경우 객체를 할당해야한다.
            answerBoarder.save() 
            return HttpResponseRedirect("answerBoardList")
        else :
            return render(request, 'answerBoarder/Board_Write.html',{'f':form,'error':'비밀번호가  8자 이상이어야 합니다.'})
    else:
        return render(request, 'answerBoarder/Board_Write.html',{'f':form,'error':'저장되지 않았습니다.'})
    # http://www.semusa.org/blog/8f82b881-3aed-44b2-a8d6-de8721880f36/
    # https://stackoverflow.com/questions/7183830/django-multiple-file-upload
def AnswerBoarderDetail(request,BOARD_NUM):
    answerBoarder = AnswerBoarder.objects.get(BOARD_NUM=BOARD_NUM);
    answerBoarder.BOARD_READCOUNT += 1
    answerBoarder.save()
    fileNames = answerBoarder.BOARD_ORIGINAL_FILENAME.split("`")
    StorefileNames = answerBoarder.BOARD_STORE_FILENAME.split("`")
    file_results = []
    for index, value in enumerate(fileNames):
        result = {}
        result['fileNames']  = value
        result['StorefileNames']  = StorefileNames[index]
        file_results.append(result)
    context = {'answerBoarder': answerBoarder, 'file_results' : file_results, 'BOARD_READCOUNT': answerBoarder.BOARD_READCOUNT}
   
    return render(request, 'answerBoarder/boarder_Detail.html', context)
    

def BoardModify(request):
    BOARD_NUM = request.GET['BOARD_NUM']
    answerBoarder = AnswerBoarder.objects.get(BOARD_NUM=BOARD_NUM)
    answerBoarder.BOARD_READCOUNT += 1
    answerBoarder.save()
    fileNames = answerBoarder.BOARD_ORIGINAL_FILENAME.split("`")
    StorefileNames = answerBoarder.BOARD_STORE_FILENAME.split("`")
    file_results = []
    for index, value in enumerate(fileNames):
        result = {}
        result['fileNames']  = value
        result['StorefileNames']  = StorefileNames[index]
        file_results.append(result)
    context = {'answerBoarder': answerBoarder, 'file_results' : file_results, 'BOARD_READCOUNT': answerBoarder.BOARD_READCOUNT}
   
    return render(request, 'answerBoarder/boarder_modify.html', context)
    #return HttpResponse("ㅁㅁㅁㅁㅁ")
    
def BoardModifyAction(request):
    if request.method == 'POST':
        BOARD_NUM = request.POST['BOARD_NUM']
        print("BOARD_NUM : " + request.POST['BOARD_NUM'])
        answerBoarder = AnswerBoarder.objects.get(BOARD_NUM=BOARD_NUM);
        print(pwEncypt(request.POST['BOARD_PASS']))
        print(answerBoarder.BOARD_PASS)
        if pwEncypt(request.POST['BOARD_PASS']) == answerBoarder.BOARD_PASS:
            print(request.POST['num'])
            if request.POST['num'] == '2':
                print(request.POST['num'])
                answerBoarder.delete()
            elif request.POST['num'] == '1':
                answerBoarder.BOARD_NAME = request.POST['BOARD_NAME']
                answerBoarder.BOARD_SUBJECT = request.POST['BOARD_SUBJECT']
                answerBoarder.BOARD_CONTENT = request.POST['BOARD_CONTENT']
                answerBoarder.save()
    return HttpResponseRedirect("answerBoardList")

def BoardReply(request):
    BOARD_NUM = request.GET['BOARD_NUM']
    answerBoarder = AnswerBoarder.objects.get(BOARD_NUM=BOARD_NUM)
    context = {'board': answerBoarder}
    return render(request, 'answerBoarder/board_reply.html', context)

from django.db import connection
def BoardReplyAction(request):
    if request.method == 'POST':
        REF = request.POST['BOARD_RE_REF']
        SEQ = request.POST['BOARD_RE_SEQ']
        print(type(REF))
        cursor = connection.cursor()
        cursor.execute("update ANSWERBOARDER set  BOARD_RE_SEQ = BOARD_RE_SEQ + 1 where BOARD_RE_REF = %s and BOARD_RE_SEQ > %s", (REF, SEQ))
        member  = Member.objects.get(USER_ID=request.session['member']['USER_ID'])
        boarderNum = AnswerBoarder.objects.aggregate(BOARD_NUM=Max('BOARD_NUM'))
        if boarderNum['BOARD_NUM'] is None:
            boarderNum['BOARD_NUM'] = 1
        else :
            boarderNum['BOARD_NUM'] += 1
        answerBoarder = AnswerBoarder()
        answerBoarder.BOARD_NUM = boarderNum['BOARD_NUM']
        answerBoarder.BOARD_NAME = request.POST['BOARD_NAME']
        answerBoarder.BOARD_PASS = pwEncypt(request.POST['BOARD_PASS'])
        answerBoarder.BOARD_SUBJECT = request.POST['BOARD_SUBJECT']
        answerBoarder.BOARD_CONTENT = request.POST['BOARD_CONTENT']
        answerBoarder.BOARD_RE_REF = int(REF)
        answerBoarder.BOARD_RE_LEV = int(request.POST['BOARD_RE_LEV']) + 1
        answerBoarder.BOARD_RE_SEQ = int(SEQ) + 1
        answerBoarder.USER_ID = member # 외래키로 지정된 경우 객체를 할당해야한다.
        answerBoarder.save()
    return HttpResponseRedirect("answerBoardList")
