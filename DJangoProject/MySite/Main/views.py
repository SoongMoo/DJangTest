from django.shortcuts import render
from django.http import HttpResponseRedirect
from member.models import Member
from .forms import SigninForm
from django.views.decorators.csrf import csrf_exempt

from member.views import pwEncypt

# Create your views here.
def index(request):
    form = SigninForm(request.POST)
    if request.COOKIES.get('autoLogin') :
        print("index  :" + request.COOKIES.get('autoLogin'))
        member = Member.objects.get(USER_ID=request.COOKIES.get('autoLogin'));
        request.session['member'] = {}
        request.session['member']['USER_ID'] = member.USER_ID
        request.session['member']['USER_PW'] = member.USER_PW
        request.session['member']['USER_NAME'] = member.USER_NAME
        request.session['member']['USER_EMAIL'] = member.USER_EMAIL
    if request.COOKIES.get('idStore') is not None :
        context = {'idStore': request.COOKIES.get('idStore')}
        form = SigninForm(initial={"USER_ID": context['idStore']})
        #form.fields['USER_ID'].initial = context['idStore']
        print("cookies111 : " + context['idStore'])
        return render(request, 'Main/main.html',  {'f':form, 'context':context})
    return render(request, 'Main/main.html', {'f':form})

def logout(request):
    response = HttpResponseRedirect("/")
    try:
        response.set_cookie('autoLogin',"111", max_age=0)
        del request.session['member']
    except KeyError:
        pass
    return response

@csrf_exempt
def loginAction(request):
    if request.method == "GET":
        return HttpResponseRedirect("/")
    elif request.method == "POST":
        id1 = request.POST['USER_ID']
        pw = request.POST['USER_PW']
        
        member = Member.objects.get(USER_ID=id1);
        print("user_ck : " + member.USER_CK)
        if member is not None:
            if member.USER_CK == '' :
                print("가입하신 이메일에서 가입승인을 먼저해주세요")
                return render(request, 'Main/main.html', {'f':SigninForm(),'error':'가입하신 이메일에서 가입승인을 먼저해주세요.'})
            
            print("회원 비밀번호 : " + member.USER_PW)
            print("입력비밀번호  : " + pwEncypt(pw))
            if member.USER_PW ==  pwEncypt(pw):
                try :
                    print(f'query')
                    request.session['member'] = {}
                    request.session['member']['USER_ID'] = member.USER_ID
                    request.session['member']['USER_PW'] = member.USER_PW
                    request.session['member']['USER_NAME'] = member.USER_NAME
                    request.session['member']['USER_EMAIL'] = member.USER_EMAIL
                    print("로그인 되었습니다." +  member.USER_ID)
                    response = HttpResponseRedirect("/")
                    if request.POST.get("idStore") is not None:
                        print("아이구여")
                        max_age = 30 * 24 * 60 * 60
                        response.set_cookie('idStore',member.USER_ID, max_age=max_age)
                    else :
                        response.set_cookie('idStore',member.USER_ID, max_age=0)
                    if request.POST.get("autoLogin") is not None:
                        max_age = 30 * 24 * 60 * 60
                        response.set_cookie('autoLogin',member.USER_ID, max_age=max_age)
                    #return HttpResponse('Thanks for your comment!')
                    return response
                except :
                    print("로그인 되지 않았습니다.")
            else :
                print("비밀번호가 틀립니다.")
                return render(request, 'Main/main.html', {'f':SigninForm(),'error':'비밀번호가 틀립니다.'})
        else :
            return render(request, 'Main/main.html', {'f':SigninForm(),'error':'아이디가 존재하지 않습니다.'})