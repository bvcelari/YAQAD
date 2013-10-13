# -*- encoding: utf-8 -*-
 
from django import forms
from news.models import Question
from news.models import Answer

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


