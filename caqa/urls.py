from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('app.views',
    # Examples:
    url(r'^$', 'home', name='home'),
    url(r'^topic_form/$', 'topic_form', name='topic_form'),
    url(r'^submit_qa/$', 'submit_qa', name='submit_qa'),
    url(r'^prev_topic/$', 'prev_topic', name='prev_topic'),
    url(r'^start_prev_topic/$', 'start_prev_topic', name='prev_topic'),

    url(r'^get_all_data/$', 'get_all_data', name='all_data'),
    url(r'^quiz/$', 'quiz', name='quiz'),
    url(r'^start/$', 'start_quiz', name='start'),
    url(r'^squiz/$', 'squiz', name='squiz'),
    url(r'^quiz_question/$','quiz_question', name='quiz_question'),
    url(r'^submit_eval/$', 'submit_eval', name='submit_eval'),
    url(r'^test/$', 'test', name='test'),
    url(r'^work/$', 'work', name='work'),
    # url(r'^caqa/', include('caqa.foo.urls')),

    url(r'^weblog/', include('zinnia.urls')),
url(r'^comments/', include('django.contrib.comments.urls')),


    url(r'', include('social_auth.urls')),
    url(r'^logout/$', 'logout_view', name='logout'),
    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
