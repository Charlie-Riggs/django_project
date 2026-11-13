from django.shortcuts import render, redirect
from MainApp.models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.      ##final exam question: get and post are the two types of requests for data
def index(request):
    return render(request, 'MainApp/index.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user)    #fetching all topic items from our database in list form (iterable)

    context = {'template_topics':topics}        #dictionary of data which we pass to our template 
                                                #key of dictionary refers to the variable name used in template
                                                #value of this dictionary is what we use in the view

    return render(request, 'MainApp/topics.html', context)

@login_required
def topic(request, topic_id):
    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        raise Http404

    if topic.owner != request.user:
        raise Http404

    entries = Entry.objects.filter(topic=topic).order_by('-date_added')    #decending order for order by is putting a negative sign in front of attribute
    context = {'topic':topic, 'entries':entries}

    return render(request, 'MainApp/topic.html', context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else: 
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('MainApp:topics')
        
    context = {'form':form}
    return render(request, 'MainApp/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        raise Http404

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm()

    else:
        form = EntryForm(data=request.POST)

        if form.is_valid():
            new_entry = form.save(commit=False)   #FOR FINAL: create the object but do not save it to the database yet
            new_entry.topic = topic
            new_entry.save()
            return redirect('MainApp:topic', topic_id=topic_id)    #need to save as a variable so the page has a topic ID
        
    context = {'form':form, 'topic':topic}
    return render(request, 'MainApp/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):       #only the things being passed from the url need to be consistent in naming
    try:
        entry = Entry.objects.get(id=entry_id)
    except Entry.DoesNotExist:
        raise Http404

    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else: 
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('MainApp:topic', topic_id=topic.id)
        
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'MainApp/edit_entry.html', context)

