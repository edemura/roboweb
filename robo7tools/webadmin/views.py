from django.shortcuts import render
from .models import ConfigType, Task
from django.template import loader
import os
from threading import Thread

# Create your views here.
from django.http import HttpResponse
from .parser2 import *
from threading import Thread
from .tasks import *

def configs(request):
    return HttpResponse(ConfigType.objects.last().write())

def poll(request):
    handler(repeat=1)
    tray_assign(repeat=1)
    task_validate(repeat=1)
    filename_generate(repeat=1)
    label_generate(repeat=1)
    send_to_robo7(repeat=1)
    #thread1 = Thread(target=handler, args=(''))
    #thread1.start()
    #thread1.join()
    return HttpResponse('running')
            
def task(request):
    task_list=Task.objects.order_by('name')    
    template = loader.get_template("task/index.html")
    context = {
        "task_list": task_list,
    }
    return HttpResponse(template.render(context, request))

def task_id(request, task_id):
    task_obj=Task(id=task_id)    
    template = loader.get_template("task/task.html")
    context = {
        "task_list": task_obj,
    }
    return HttpResponse(template.render(context, request))

def task_run(request, task_id):
    pass 

def task_stop(request, task_id):
    pass  

def stop(request):
    pass

def dir(request):
    return HttpResponse(os.listdir(path='get'))

