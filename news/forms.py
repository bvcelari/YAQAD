# -*- encoding: utf-8 -*-
 
from django import forms
from news.models import Question


class AddQuestionForm(forms.ModelForm):
  class Meta:
    model = Question
    fields = ('title', 'subtitle','content')
