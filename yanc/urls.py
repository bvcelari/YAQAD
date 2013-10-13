from django.conf.urls import patterns, include, url
from news import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yanc.views.home', name='home'),
    # url(r'^yanc/', include('yanc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
        url(r'^index/$', 'news.views.index'),
        url(r'^login/$', 'news.views.mylogin'),
        url(r'^logout/$', 'news.views.log_me_out'),
        url(r'^addquestion/$', 'news.views.add_question'),
        url(r'^ajaxaddquestion/$', 'news.views.ajax_add_question'),
        url(r'^ajaxaddanswer/$', 'news.views.ajax_add_answer'),
	#url(r'^(?P<question_id>\d+)/$',  'news.views.question',name = 'question'),
	url(r'^(?P<question_id>\d+)/(?P<slug>[-\w]+)/$',  'news.views.question'),


)
