from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Member
from datetime import datetime
from .forms import SignupForm
from django.http.response import HttpResponseNotFound

# Create your views here.

def agree(request):
    return render(request, 'member/agree.html')

@csrf_exempt
def regist(request):
    if request.method == "GET":
        return HttpResponseRedirect("agree")
    elif request.method == "POST" :
        agree = request.POST.get("agree")
        if agree is not None :
            return render(request, 'member/memberForm.html',{'f':SignupForm()})
        else :
            return HttpResponseRedirect("agree")

@csrf_exempt
def memberJoinAction(request):
    if request.method == "GET":
        return HttpResponseRedirect("agree")
    elif request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['USER_PW']  == form.cleaned_data['USER_PW_Con']:
                member = Member()
                member.USER_ID = form.cleaned_data['USER_ID']
                member.USER_PW = pwEncypt(form.cleaned_data['USER_PW'])
                member.USER_NAME = form.cleaned_data['USER_NAME']
                member.USER_BIRTH = form.cleaned_data['USER_BIRTH']
                member.USER_GENDER = form.cleaned_data['USER_GENDER']
                member.USER_EMAIL = form.cleaned_data['USER_EMAIL']
                member.USER_ADDR = form.cleaned_data['USER_ADDR']
                member.USER_PH1 = form.cleaned_data['USER_PH1']
                member.USER_PH2 = form.cleaned_data['USER_PH2']
                member.USER_REGIST = datetime.now()
                print(pwEncypt(form.cleaned_data['USER_PW']))
                try:
                    mailSend(member)
                    member.save()
                    print("저장되었습니다.")
                    return HttpResponseRedirect("/")
                except :
                    return HttpResponseNotFound("가입되지 않았습니다.")
                    #return render(request, 'member/memberForm.html',{'f':form,'error':'가입되지 않았습니다.'})    
            else :
                return render(request, 'member/memberForm.html',{'f':form,'error':'비밀번호 확인이  비밀번호와 다릅니다.'})
        else :
            return render(request, 'member/memberForm.html',{'f':form,'error':'가입되지 않았습니다.'})
        
   
from django.core.mail import EmailMultiAlternatives
import uuid

def mailSend(member):
    num = str(uuid.uuid1()).replace('-', '')
    print(num)
    content = "<html><body>안녕하세요 가입을 환영합니다. 아래 링크를 누르셔야만 가입이 완료됩니다.<br />" 
    content += "<a href='http://localhost:8000/member/memberMail/" + num 
    content += "?email=" + member.USER_EMAIL + "'> 클릭 </a></body></html>"
    subject = "가입환영인사";
    from_email = 'hiland00@gmail.com'
    to = member.USER_EMAIL
    
    msg = EmailMultiAlternatives(subject, content, from_email, [to]) 
    msg.attach_alternative(content, "text/html")
    msg.send()   
    

def memberMail(request, USER_CK):
    USER_EMAIL = request.GET['email']
    member = Member.objects.get(USER_EMAIL = USER_EMAIL)
    try:
        if member.USER_CK == '' :
            member.USER_CK = USER_CK
            member.save()
            return render(request, 'member/memberMailTrue.html')
        else : 
            return render(request, 'member/memberMailFalse.html')
    except:
        pass
    
import hashlib
def pwEncypt(USER_PW):
    result = hashlib.sha256(USER_PW.encode())
    return result.hexdigest()
    


def memberDetail(request):
    USER_ID = request.session['member']['USER_ID']
    member = Member.objects.get(USER_ID=USER_ID);
    context = {'member': member}
    return render(request, 'member/memberDetail.html', context)
    #return HttpResponse(member.USER_ID)      
         
def memberModify(request):
    USER_ID = request.session['member']['USER_ID']
    member = Member.objects.get(USER_ID=USER_ID);
    context = {}
    try:
        request.GET['num']
        context = {'member': member , 'error':'비밀번호가  틀렸습니다.'}
    except:
        context = {'member': member}
    return render(request, 'member/memberModify.html', context)
        
@csrf_exempt
def memberModifyPro(request): 
    print("수정페이지입니다.")
    userId = request.session['member']['USER_ID']
    userPw = pwEncypt(request.POST['USER_PW'])       
    print("memberModifyPro : " + userId)
    print("memberModifyPro : " + userPw)
    try:    
        member = Member.objects.get(USER_ID = userId, USER_PW = userPw)
        print("사용자입니다.")
        member.USER_BIRTH = request.POST['USER_BIRTH'] 
        member.USER_EMAIL = request.POST['USER_EMAIL'] 
        member.USER_ADDR = request.POST['USER_ADDR'] 
        member.USER_PH1 = request.POST['USER_PH1'] 
        member.USER_PH2 = request.POST['USER_PH2'] 
        member.save()
        return HttpResponseRedirect("memberDetail")
    except:
        print("비밀번호가  틀렸습니다.")
        return HttpResponseRedirect("memberModify?num=1")
     
def changePassword(request):
    return render(request, 'member/memberPassword.html')
    #return HttpResponse("ㅁㅁㅁㅁㅁ")  
    
def memberPasswordPro(request):
    userId = request.session['member']['USER_ID']
    userPw = pwEncypt(request.POST['USER_PW'])   
    try:    
        member = Member.objects.get(USER_ID = userId, USER_PW = userPw)
        return render(request, 'member/memberPasswordPro.html')
    except:
        return render(request, 'member/memberPassword.html',{'error':'비밀번호가  틀렸습니다.'})
    return HttpResponse("ㅁㅁㅁㅁㅁ")
 
@csrf_exempt                
def memberPasswordModifyPro(request):
    userId = request.session['member']['USER_ID']
    userPw = pwEncypt(request.POST['USER_PW_CRRUNT']) 
    USER_PW_NEW = request.POST['USER_PW_NEW']
    USER_PW_RE_NEW = request.POST['USER_PW_RE_NEW']
    if USER_PW_NEW != USER_PW_RE_NEW :
        return render(request, 'member/memberPasswordPro.html', {'error':'새 비밀번호와 비밀번호 확인이  다릅니다.'})
    else:
        try:
            member = Member.objects.get(USER_ID = userId, USER_PW = userPw)
            userNewPw = pwEncypt(USER_PW_NEW)
            member.USER_PW = userNewPw
            member.save()
            print("비밀번호가 변경되었습니다.")
            return HttpResponseRedirect("memberDetail")
        except:
            print("비밀번호를 잘 못 입력하였습니다.")
            return render(request, 'member/memberPasswordPro.html', {'error':'비밀번호를 잘 못 입력하였습니다.'})


from django.core.paginator import Paginator
import math
def memberlist(request):
    page = request.GET.get('page',1)
    limit = 4
    page_range = 10
    members = Member.objects.all().order_by('-USER_REGIST')        # order_by('-fild_name') : 내림차순
    print(str(members.query))
    paginator = Paginator(members, limit)
    contacts = paginator.get_page(page)
    
    current_block = math.ceil(int(page)/page_range)
    start_block = (current_block-1) * page_range
    end_block = start_block + page_range
    p_range = paginator.page_range[start_block:end_block]
    
    print(p_range)
    
    context = {'contacts': contacts,'p_range' : p_range,}
    return render(request, 'member/memberList.html',context)    

def memberInfo(request, USER_ID):
    member = Member.objects.get(USER_ID = USER_ID)
    context = {'member': member,'num' : 1}
    return render(request, 'member/memberDetail.html', context)
    #return HttpResponse("ㅁㅁㅁㅁㅁ")


def memberDelete(request):
    userId = request.session['member']['USER_ID']
    member = Member.objects.get(USER_ID = userId)
    member.delete ()
    return HttpResponseRedirect("/logout")



