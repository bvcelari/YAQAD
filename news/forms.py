# -*- encoding: utf-8 -*-
 
from django import forms
from news.models import Question
from news.models import Answer
from news.models import Topic

class AddQuestionForm(forms.ModelForm):
  class Meta:
    model = Question
    fields = ('title','content')
    widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Add your question'}),
            'content': forms.Textarea(attrs={'placeholder': 'Add more information'}),
        }


class AddAnswerForm(forms.ModelForm):
  class Meta:
    model = Answer
    fields = ('answer_content',)
    widgets = {
            'answer_content': forms.Textarea(attrs={'placeholder': 'Add your answer'}),
        }


class TopicForm(forms.ModelForm):
	name  = forms.CharField(max_length=100, help_text='type topic')
	class Meta:
        	model = Topic
        	fields=('name',)
		widgets = {
         	   'name': forms.Textarea(attrs={'placeholder': 'Add a Topic'}),
        	}

#	def __init__(self, *args, **kwargs):
#        	super(TopicForm, self).__init__(*args, **kwargs)
#        	self.field['topic'].label = "Add a Topic"
