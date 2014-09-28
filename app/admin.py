from app.models import *
from django.contrib import admin



class TopicAdmin(admin.ModelAdmin):
    list_display = ['topic','subject','sub_topics','date_created','last_modified']
    ordering = ['id']


class QADataAdmin(admin.ModelAdmin):
    list_display = ['topic','question','answers','date_created']
    ordering = ['id']


class QuizAdmin(admin.ModelAdmin):

    list_display = ['topic','efficency','date_taken']
    ordering = ['id']
admin.site.register(Topic,TopicAdmin)
admin.site.register(QAData,QADataAdmin)
admin.site.register(Quiz,QuizAdmin)
