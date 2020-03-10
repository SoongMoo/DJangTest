from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Candidate, Poll, Choice #models에 정의된 Candidate를 import 
from django.http import HttpResponseNotFound #추가
from django.http import Http404 
from django.shortcuts import get_object_or_404

import datetime

from django.db.models import Sum 

def index(request):
    candidates = Candidate.objects.all()       #Candidate에 있는 모든 객체를 불러옵니다
    context = {'candidates' : candidates}
    return render(request, 'elections/index.html',context)


def candidates(request, name):
	try :
		candidate = Candidate.objects.get(name = name)
	except:
		raise Http404
	return HttpResponse(candidate.name)

def areas(request, area): 
	today = datetime.datetime.now() # 현재시간 가져오기
	# Poll에 있는 데이터가 현재시간이 시작시간과 종료시간 사이에 있는지 비교해야 한다.
	try:
		poll = Poll.objects.get(area = area, start_date__lte= today, end_date__gte=today)
		candidates = Candidate.objects.filter(area = area)
	except:
		poll = None
		candidates = None
	context = {'candidates': candidates, 'area' : area, 'poll' : poll}
	return render(request, 'elections/area.html',context)


def polls(request, poll_id):
	poll = Poll.objects.get(pk = poll_id)
	selection = request.POST['choice']

	try:
		choice = Choice.objects.get(poll_id = poll.id, candidate_id = selection)
		choice.votes += 1
		choice.save()
	except:
		#최초로 투표하는 경우, DB에 저장된 Choice객체가 없기 때문에 Choice를 새로 생성합니다
		choice = Choice(poll_id = poll.id, candidate_id = selection, votes = 1)
		choice.save()
	#return HttpResponse("finish") #여기 지우고
	return HttpResponseRedirect("/areas/{}/results".format(poll.area)) #  ①


def results(request, area):  # ②

	candidates = Candidate.objects.filter(area = area) 

	polls = Poll.objects.filter(area = area)  # ② 여론조사에 대한 정보를 가져온다.
	poll_results = []  # ③ 기간별로 여러개의 여론조사의 기간이 있을 수 있으므로 리스트로 만든다.
	for poll in polls:
		result = {} # ④ 딕셔러리를 만들어 준다.
		result['start_date'] = poll.start_date
		result['end_date'] = poll.end_date

		total_votes = Choice.objects.filter(poll_id = poll.id).aggregate(Sum('votes'))
		print("######", total_votes )

		result['total_votes'] = total_votes['votes__sum']

		rates = [] #지지율
		for candidate in candidates:
			# choice가 하나도 없는 경우 - 예외처리로 0을 append
			try:
				choice = Choice.objects.get(poll = poll, candidate = candidate)
				rates.append(
					round(choice.votes * 100 / result['total_votes'], 1)
					)
			except :
				rates.append(0)
		result['rates'] = rates
		poll_results.append(result)

	context = {'candidates':candidates, 'area':area,'poll_results' : poll_results}
	return render(request, 'elections/result.html', context)
# Create your views here.
