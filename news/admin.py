# encoding: utf-8
from django.contrib import admin
from news.models import Answer, AnswerLikes, Question, Fedder, Topic

class AnswerLikesAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, 
			{'fields':('answer_like','question_like','owner_like'),}
		)
	]
	list_display=('answer_like','question_like','owner_like')
admin.site.register(AnswerLikes,AnswerLikesAdmin)	
class AnswerAdmin(admin.ModelAdmin): 
	fieldsets = [
		(None,
			{'fields':('writer','answer_content','likes'),}
		)
	]
	list_display=('writer','answer_content','likes') 
admin.site.register(Answer,AnswerAdmin)

##This should be logicaly Managed, no here
#class AnswerLikesAdmin(admin.ModelAdmin): 
#	fieldsets = [
#		(None,
#			{'fields':('',),}
#		)
#	]
#	list_display=('',) 
#admin.site.register(AnswerLikes,AnswerLikesAdmin)

class QuestionAdmin(admin.ModelAdmin): 
	def formfield_for_dbfield(self, db_field, **kwargs):
	      return super(QuestionAdmin, self).formfield_for_dbfield(db_field, **kwargs)
	list_display = ('title', 'excerpt', 'publication_date', 'owner')
	prepopulated_fields = { 'machine_name' : ('title', ) }
        filter_horizontal = ('answer',)
	list_filter = ['publication_date', 'owner']
	date_hierarchy = 'publication_date'
	search_fields = ['title', 'content', 'owner__username', 'owner__first_name', 'owner__last_name']
admin.site.register(Question,QuestionAdmin)

class FedderAdmin(admin.ModelAdmin): 
	fieldsets = [
		(None,
			{'fields':('fedder','name','surname','email','questions','answers',),}

		)
	]
        filter_horizontal = ('questions','answers',)
	list_display=('fedder','name','surname','email',) 
admin.site.register(Fedder,FedderAdmin)

class TopicAdmin(admin.ModelAdmin): 
	fieldsets = [
		(None,
			{'fields':('name',),}
		
		)
	]
	list_display=('name',) 
admin.site.register(Topic,TopicAdmin)

