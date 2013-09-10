# encoding: utf-8
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from news.forms import AddQuestionForm
from news.models import Question




@login_required(login_url='/login/')
def add_question(request):
	state = 1
        logged_user = request.user
        if logged_user.is_active:
		#Should separate this in Helper functions...
		addquestionform = AddQuestionForm()
		if request.POST:
			addquestionform =AddQuestionForm(request.POST)
			if addquestionform.is_valid():
				addquestion = addquestionform.save(commit=False)
				addquestion.owner_id = logged_user.id
				addquestion.save()
				#I guess that should miss Slug field, date.. all the other staff
				state = 2

	return render_to_response('addquestion.html',
                {
                        'state':state,
                        'addquestionform':addquestionform,
                },
                context_instance=RequestContext(request))


def index(request):
        state = 0
        username = ''
        if request.user:
        	logged_user = request.user
                if logged_user.is_active:
		    	state = 1
			#Lets show your more recents Questions...
			question_list=Question.objects.filter(owner_id=logged_user.id).order_by("publication_date").reverse()[:3]
			#this are the related answers :  question_list[0].answer.count()
			if question_list.exists() is False:
				question_list=''
			#we add the question form...
			addquestionform = AddQuestionForm()
			if request.POST:
	                        addquestionform =AddQuestionForm(request.POST)
	                        if addquestionform.is_valid():
	                                addquestion = addquestionform.save(commit=False)
	                                addquestion.owner_id = logged_user.id
	                                addquestion.save()
	                                #I guess that should miss Slug field, date.. all the other staff
	                                state = 2
	else:
		question_list=''

        return render_to_response('index.html',
		{
			'request':request,
                        'username': username,
                        'logged_user':logged_user,
                        'state':state,
                        'question_list':question_list,
                        'state':state,
                        'addquestionform':addquestionform,
		},
		context_instance=RequestContext(request))


def mylogin(request):
        state = 0
        username = ''
        logged_user = ''

        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    logged_user = request.user
		    state = 1
	
	else:
                username = ''
                state = 0

        return render_to_response('mylogin.html',
                {
                        'username': username,
                        'logged_user':logged_user,
                        'state':state,
                },
                context_instance=RequestContext(request))


def log_me_out(request):
        logout(request)
        return redirect('/index/')

