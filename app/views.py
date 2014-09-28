
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render_to_response
from django.shortcuts import render_to_response, redirect
import django.utils.timezone
from django.contrib.auth import logout
from app.models import *
import datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required


import json

def home(request):
    print request.user
    user = request.user
    print "uu",user
    if user.is_authenticated():

        topic = Topic.objects.filter(user = user)
        return render_to_response('index.html',{'topics':topic},context_instance=RequestContext(request))
    else:
        return render_to_response('login.html',{},context_instance=RequestContext(request))

def logout_view(request):
    user = request.user
    print "us",user.id
    if user.is_authenticated():

        return render_to_response('login.html',{},context_instance=RequestContext(request))
def topic_form(request):
    
    user = request.user
    topic = request.POST.get('topic','')
    sub_topic = request.POST.get('sub_topic_list','')
    subject  = request.POST.get('subject','')
    topic_check = Topic.objects.filter(topic = topic,sub_topics = sub_topic,user=user)
    if topic_check:
        topic_details = topic_check[0]
        print "I am Not Saving"
    else:
        tpc = Topic()
        tpc.user = user
        tpc.subject = subject
        tpc.topic = topic
        tpc.sub_topics = sub_topic
        tpc.date_created = datetime.datetime.now()
        tpc.last_modified = datetime.datetime.now()

        tpc.save()
        print "I am Saving"
        topic_details = Topic.objects.get(id = tpc.id)

    sub_topics_list = []
    if topic_details.sub_topics:
        sub_topics_list = topic_details.sub_topics.split(";")

    qadata = QAData.objects.filter(topic__id = topic_details.id)
    count_data = len(qadata)
    return render_to_response('qaportal.html',{'tpc':topic_details, "sub_topics":sub_topics_list,'count_data':count_data},context_instance=RequestContext(request))




def submit_qa(request):
    
    question = request.POST.get('questions','')
    answers = request.POST.get('answers','')
    topic_id = request.POST.get('topic_id','')
    topic_details = Topic.objects.get(id = topic_id)

    print "QU", topic_details.topic

    qad = QAData()
    qad.question = question + "?"
    qad.answers = answers
    qad.topic = topic_details
    qad.date_created = datetime.datetime.now()
    topic_details.last_modified = datetime.datetime.now()
    qad.save()
    topic_details.save()
    qadata = QAData.objects.filter(topic__id = topic_id)
    count_data = len(qadata)

    
    return HttpResponse(json.dumps(count_data), mimetype="application/json")



def squiz(request):
    user = request.user
    count_data = 5
    topic = request.POST.get('tpc_name','')
    qadata = QAData.objects.filter(topic__topic = topic, topic__user = user).order_by('date_created').reverse()
    if qadata:
        fques = {'question':qadata[0].question,'fid':qadata[0].id}
        
    else:
        fques = "No Question "

    return HttpResponse(json.dumps(fques), mimetype="application/json")


def quiz_question(request):

    user = request.user
    qids = request.POST.get('qids','')
    qids = str(qids)
    qids_list = qids.split(",")
    qids_list.pop(-1)
    topic = request.POST.get('tpc_name','')
    qadata = QAData.objects.filter(topic__topic = topic, topic__user = user).order_by('date_created').reverse()
    qids_list = map(int,qids_list)
    for value in qadata:
        if value.id not in qids_list:
           fques = {'question':value.question,'fid':value.id}
           break;

    if len(qids_list) >= len(qadata):
        fques = {'question':"No Question Left Please Submit The test ",'fid':'zz'}
    return HttpResponse(json.dumps(fques), mimetype="application/json")


def submit_eval(request):

    qans_list = request.POST.get('qans_list','')
    qans_list = str(qans_list)
    qans_list = qans_list.split(";")
    qans_list.pop(-1)
    print qans_list
    qdict = eval(qans_list[0])

    res_list = []
    num = 0
    for value in qans_list:

        val_dict = eval(value)
        print "dI", val_dict
        print type(val_dict)
        qadata = QAData.objects.get(id = val_dict['qid'])
        print "A", qadata.answers
        print "B", val_dict['answer']
        if qadata.answers.upper() == val_dict['answer'].upper() :
            result = "correct"
            num += 1
        else:
            result = "Incorrect"

        res_dict = {'qadata':qadata, 'yans':val_dict['answer'], 'result':result}

        res_list.append(res_dict)
    

    print res_list
    perce = float(num)/len(qans_list)
    perce *= 100
    print "Pe%", perce
    try:
        qz = Quiz()
        qz.topic = qadata.topic
        qz.efficency = perce
        qz.date_taken = datetime.datetime.now()
        qz.save()

    except:
        print "Not Saved"

    return render_to_response('result.html',{'res_list':res_list,'attempted':len(qans_list),'correct':num, 'perce':perce},context_instance=RequestContext(request))

def start_quiz(request):
    count_data = 5
    return HttpResponse(json.dumps(count_data), mimetype="application/json")




def prev_topic(request):
    user = request.user
    topic_name = request.POST.get('ftopic','')
    topics = Topic.objects.filter(topic = topic_name, user = user)
    topic_details = []
    for values in topics:
        sub_topics_list = values.sub_topics.split(";")
        topic_details.append({'topic_id':values.id,'sub_topics':sub_topics_list,'date_modified':values.last_modified})


    print "TD", topic_details

    return render_to_response('topic_list.html',{'topic_dict':topic_details,'topic_name':topic_name},context_instance=RequestContext(request))


def start_prev_topic(request):
    topic_id = request.POST.get('topic_id','')
    submit_type = request.POST.get('submit_type','')
    print "submit_type"
    topics = Topic.objects.get(id = topic_id)
    qadata = QAData.objects.filter(topic__id = topic_id)
    count_data = len(qadata)

    if topics.sub_topics:
        sub_topics_list = topics.sub_topics.split(";")

    if submit_type == "start":
        return render_to_response('qaportal.html',{'tpc':topics, "sub_topics":sub_topics_list,'count_data':count_data},context_instance=RequestContext(request))

    elif submit_type == "qa":
        return render_to_response('qadisp.html',{'qadata':qadata,"sub_topics":sub_topics_list,'topic_name':topics.topic},context_instance=RequestContext(request))



def get_all_data(request):

    user = request.user
    topic_name = request.POST.get('topic_name','')
    qadata = QAData.objects.filter(topic__topic = topic_name, topic__user = user)
        
    return render_to_response('qadisp.html',{'qadata':qadata,'topic_name':topic_name},context_instance=RequestContext(request))

def test(request):
       
    return render_to_response('test.html',{},context_instance=RequestContext(request))


def quiz(request):
    return render_to_response('quiz.html',{},context_instance=RequestContext(request))



def work(request):
    return render_to_response('work.html',{},context_instance=RequestContext(request))
