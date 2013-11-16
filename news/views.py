# encoding: utf-8
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from news.forms import AddQuestionForm
from news.forms import AddAnswerForm
from news.models import Question
from news.models import Answer
from news.models import Fedder
## needed by ajax
from django.http import HttpResponse  
from django.template.loader import render_to_string  
from django.utils import simplejson  
from django.utils.functional import Promise  
from django.utils.encoding import force_unicode  
## end needed by ajax
# I am sure that there is a better way than state flags to check where are we
#0 = logout
#1 = login 
#2 = result form

def ajax_add_topics(request):
	result = []
	if request.method == "GET":
	    if request.GET.has_key(u'query'):
	        value = request.GET[u'query']
	        # Ignore queries shorter than length 3
	        if len(value) > 2:
	            model_results = Topic.objects.filter(name__icontains=value)
	            results = [ x.name for x in model_results ]
	json = simplejson.dumps(results)
	return HttpResponse(json, mimetype='application/json')


login_required(login_url='/login/')
def question(request,question_id,slug):
	state=1
        result = ''
	myquestion=''
	addquestionform = ''
	addanswerform = ''
        logged_user = request.user
        if logged_user.is_active:
		state=1
		myquestion = Question.objects.get(id=question_id)
                #Should separate this in Helper functions...
                addquestionform = AddQuestionForm()
                addanswerform = AddAnswerForm()
                if request.POST:
                        addquestionform =AddQuestionForm(request.POST)
                        if addquestionform.is_valid():
                                addquestion = addquestionform.save(commit=False)
                                addquestion.owner_id = logged_user.id
                                addquestion.save()
                                #I guess that should miss Slug field, date.. all the other staff
                                state = 2




        return render_to_response('question.html',
                {
                        'logged_user':logged_user,
                        'state':state,
                        'myquestion':myquestion,
                        'addquestionform':addquestionform,
                        'addanswerform':addanswerform,
                },
                context_instance=RequestContext(request))

@login_required(login_url='/login/')
#def ajax_add_answer(request,answer_content, question_id):
def ajax_add_answer(request):
        result = ''
        state = 1
        logged_user = request.user
        if logged_user.is_active:
                #Should separate this in Helper functions...
                addanswerform = AddAnswerForm()
                if request.POST:
                   if request.is_ajax():
                        addanswerform =AddAnswerForm(request.POST)
                        if addanswerform.is_valid():
                                addanswer = addanswerform.save(commit=False)
                                addanswer.writer_id = logged_user.id
                                myanswer= addanswer.save()
				#TODO: question_id is hardcoded in base.html ... find a better way
				myquestion=Question.objects.get(id=request.POST['question_id'])
				myquestion.answer.add(addanswer.id)
				myquestion.save()
                                state = 2
                                result = simplejson.dumps({
                                        'message': "Success message",
                                        'message_type': 'success',
                                        'response': "Your answer have been added",
                                        })
                                result = "Your answer have been added..."

        return HttpResponse(result)



@login_required(login_url='/login/')
def ajax_add_question(request):
	result = ''
        state = 1
        logged_user = request.user
        if logged_user.is_active:
                #Should separate this in Helper functions...
                addquestionform = AddQuestionForm()
                if request.POST:
		   if request.is_ajax():  
                        addquestionform =AddQuestionForm(request.POST)
                        if addquestionform.is_valid():
                                addquestion = addquestionform.save(commit=False)
                                addquestion.owner_id = logged_user.id
                                addquestion.save()
				print(logged_user.id)
				writer= Fedder.objects.get(fedder=logged_user.id)
				writer.questions.add(addquestion.id)
                                state = 2
				result = simplejson.dumps({  
					'message': "Success message", 
				        'message_type': 'success',
				        'response': "Your question have been added",
				        })
				result = "Your question have been added..."
				
	return HttpResponse(result)

       # return render_to_response('addquestion.html',
       #         {
       #                 'state':state,
       #                 'addquestionform':addquestionform,
       #         },
       #         context_instance=RequestContext(request))



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
                                writer= Fedder.objects.get(fedder=logged_user.id)
                                writer.questions.add(addquestion.id)
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
	question_list=''
        addquestionform=''
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



