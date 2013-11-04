# encoding: utf-8
from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User

from django.template.defaultfilters import slugify

#Inbox mail system,notifications....
#think about follower and following... and how to handle big numbers...
#think about what is shareable, and think about what is commentable

#	Topics are independents and define Questions
#	about a Topic, you can write a review or.. you can write a post.

#	Answers has likes... 
#	Answer has comments... 
#	likes = models.PositiveIntegerField(blank=True)
class Topic(models.Model):
	name = models.TextField(unique=True)
        def __unicode__(self):
          return str(self.name)

	

class Answer(models.Model):
	#should an user make more than one answer?
	#writer can not be unique... is not an id.. should be cool a uniqes pair of writer question to search quickly
	writer = models.ForeignKey(User)
	answer_content = models.TextField(blank=True)
	likes = models.PositiveIntegerField(blank=True,default=0)
	#TODO:Date should be recorded when was added

        def __unicode__(self):
          return str(self.writer) + ' - ' +self.answer_content[:300] + u'…'

#this class, give you fast access to how like what
class AnswerLikes(models.Model):
	answer_like = models.OneToOneField(Answer)
	owner_like = models.OneToOneField(User)

class Question(models.Model):
#	Questions has Topics
#	Can a questions owner write an answer?
	title = models.CharField(max_length=255)
	subtitle = models.CharField(max_length=255,blank=True)
#	machine_name = models.SlugField(max_length=255, primary_key=True)
	machine_name = models.SlugField(max_length=255)
	content = models.TextField(blank=True)
	publication_date = models.DateTimeField(null=True,blank=True,auto_now_add=True)
	answer = models.ManyToManyField(Answer,unique=False,blank=True)
#	collapsed = this should have... when and who closed it?
	owner = models.ForeignKey(User)
	topics = models.ManyToManyField(Topic, unique=False)
	def save(self, *args, **kwargs):
	  self.machine_name = slugify(self.title)
	  super(Question, self).save(*args, **kwargs)

	def __unicode__(self):
	  return self.title
	
	def excerpt(self):
	  return self.content[:300] + u'…'

#This shoould do the trick with urls and the view questiondetails
#	def get_absolute_url(self):
#	  from django.core.urlresolvers import reverse
#	  return reverse('questiondetails',kwargs={ 'slug':self.machine_name })
	
	class Meta:
	  ordering = [u'-publication_date']

class Fedder(models.Model):
	fedder = models.ForeignKey(User, unique=True)
        name = models.CharField(max_length=30,blank=True)
        surname = models.CharField(max_length=30,blank=True)
        email = models.EmailField()
        questions = models.ManyToManyField(Question, unique=False,blank=True,null=True)
        answers = models.ManyToManyField(Answer, unique=False,blank=True,null=True)
        #likes = models.ForeignKey(AnswerLikes, unique=False)
        ## TODO:You have to implement a file uploader for image ...


        def __unicode__(self):
            return unicode(self.name)

