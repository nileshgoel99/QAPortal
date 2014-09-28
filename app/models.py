from django.db import models

from django.contrib.auth.models import User
# Create your models here.


class Topic(models.Model):

    user = models.ForeignKey(User, null=True, blank=True)
    subject = models.CharField(max_length=500, blank=True)
    topic =models.CharField(max_length=500, blank=True)
    sub_topics = models.CharField(max_length=500, blank=True)
    date_created = models.DateTimeField(null=True, blank=True)
    last_modified = models.DateTimeField(null=True, blank=True)
    check = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return '%s:%s' %(self.topic, self.date_created)

class QAData(models.Model):

    topic = models.ForeignKey(Topic, null=True, blank=True)
    question = models.CharField(max_length=1000, blank=True)
    answers = models.CharField(max_length=2000, blank=True)
    date_created = models.DateTimeField(null=True, blank=True)

class Quiz(models.Model):

    topic = models.ForeignKey(Topic, null=True, blank=True)
    efficency = models.CharField(max_length=500, blank=True)
    date_taken = models.DateTimeField(null=True, blank=True)


