import os
from .parser2 import * 
from .models import Config, ConfigType, Robo7Task, Analysis, AnalysisSet, TrayTube, Filename, Label
from background_task import background
from datetime import datetime, date, timedelta

#Задача - проверка в папке файла с виртуального принтера, формирование задания
@background(schedule=1, queue='my-queue', remove_existing_tasks=True)
def handler(repeat=1):
    print('1. task parsing is running')
    path=r'C:\\roboweb\robo7tools\webadmin\get'
    if len(os.listdir(path=path))!=0:
        
            for filename in os.listdir(path=path):
                #if filename.find(".pdf")!=-1:
                if os.path.exists((path+'\\'+filename)) and filename.find(".pdf")!=-1:
                    dict=parse_tasks((path+'\\'+filename))
                    for i in dict:
                        fio=i.get('fio')
                        analysis=i.get('analysis')
                        code=i.get('code')
                        ctype=(str(code)[3:-1]).replace(' ','_').replace('.','')
                        #task=Task(fio=fio, analisys=analysis, code=code)
                        tsk=Robo7Task(patient_fio=fio, code=ctype, analysis=analysis, tray_num=0)
                        '''
                        try:
                            prev = Robo7Task.objects.order_by('-create_datetime')[0]
                            
                            if tsk.create_datetime.date()==prev.create_datetime.date():
                                tsk.tray_num_task=prev.tray_num_task+1
                            else:
                                tsk.tray_num_task=1
                        except:
                            tsk.tray_num_task=1
                        '''
                        tsk.tray_num_task=1
                        tsk.save()
                        #cfg=ConfigType(configtype=ctype)
                        #cfg.save()
                    os.remove((path+'\\'+filename))

#Присвоение заданиям номеров лотков, в которых находится подходящий тип пробирки
@background(schedule=1, queue='my-queue', remove_existing_tasks=True)
def tray_assign(repeat=1):
    print('2. tray assign is running')
    for i in Robo7Task.objects.filter(is_tray_assigned=(False or None)):
        an=Analysis.objects.filter(set=AnalysisSet.objects.get(active=True), analysis_name=i.analysis)
        tube_type=an[0].tube_type
        tray_tube=TrayTube.objects.filter(tube_type=tube_type)[0]
        if tray_tube!=None:
            i.tray_num=tray_tube.tray
            i.is_tray_assigned=True
        else:
            i.is_tray_assigned=False
        i.save()

    # for i in Robo7Task.objects.all():
    
    #     i.is_tray_assigned=False
    #     i.save()

#Валидция задачи
@background(schedule=1, queue='my-queue', remove_existing_tasks=True)
def task_validate(repeat=1):
    checkhours=2
    now=datetime.now()
    chkdate=now-timedelta(hours=checkhours)
    print('3. task validation is running')
    for i in Robo7Task.objects.filter(is_tray_assigned=True, is_validated=(False or None)):
        fio=i.patient_fio
        analysis=i.analysis
        code=i.code
        tray=i.tray_num
        similartask=Robo7Task.objects.filter(is_tray_assigned=True, is_validated=True, 
                        patient_fio=fio, analysis=analysis, code=code, tray_num=tray, create_datetime__gt=chkdate)
        #ttoday=Robo7Task.objects.filter(create_datetime__date=i.create_datetime.date)
        if similartask is None:
            i.is_validated=True

        else:
            #i.is_validated=False
            i.is_validated=True
        i.save()

#Формирование имени файла
@background(schedule=1, queue='my-queue', remove_existing_tasks=True)
def filename_generate(repeat=1):
    print('4. filename generating is running')
    for j in Robo7Task.objects.filter(is_validated=True):

        name=Filename()
        name.date=datetime.now().strftime('%m%d')
        #name.patient_name=j.patient_fio
        name.stocker_code='0'+str(j.tray_num)
        name.tray_number=(4-len(str(j.tray_num_task)))*0+str(j.tray_num_task)

        filename=name.make()
        filenameok=name.makeok()
        

        if filename!=None:
            j.filename=filename
            j.filenameok=filenameok
            j.is_filename=True
            j.save()
        else:
            j.is_filename=False
            j.save()

#Формирование этикетки
@background(schedule=1, queue='my-queue', remove_existing_tasks=True)
def label_generate(repeat=1):
    print('5. label generating is running')
    for j in Robo7Task.objects.filter(is_validated=True):

        label=Label()
        label.barcode_data=j.code


        labeltext=label.make()
        

        if labeltext!=None:
            j.label=labeltext
            j.is_label=True
            j.save()
        else:
            j.is_label=False
            j.save()

#Отправка задания на robo7
@background(schedule=1, queue='my-queue', remove_existing_tasks=True)
def send_to_robo7(repeat=1):
    print('6. sending to robo7 is running')
    #folder='out'
    folder=r'C:\\robo7_data\PRINT\DATA'
    for j in Robo7Task.objects.filter(is_filename=True, is_label=True, is_sent=(False or None)):
        
        try:    
            with open(folder+'\\'+j.filename+'.dat','w') as file:
                file.write(j.label)
                file.close()

            with open(folder+'/'+j.filename+',DEF.TXT','w') as file:
                file.write('')
                file.close()

            j.is_sent=True
            j.save()
        except:
            j.is_sent=False
            j.save()


#Проверка выполнения задач прибором
@background(schedule=1, queue='my-queue', remove_existing_tasks=True)
def check_robo7_complete(repeat=1):
    print('7. Checking comliance of robo7 tasks is running')
    folder='out'
    for j in Robo7Task.objects.filter(is_sent=True):
        

        #path=r'C:\\roboweb\robo7tools\webadmin\get'
        path=r'C:\\robo7_data\PRINT\DATA'
        if len(os.listdir(path=path))!=0:
                
            #for filename in os.listdir(path=path):
            
                if os.path.exists((folder+'\\'+j.filenameok))!=-1:

                    try:    
                        os.remove((folder+'\\'+j.filenameok))
                        os.remove((folder+'\\'+j.filename+'.dat'))
                        os.remove((folder+'\\'+j.filename+',DEF.TXT'))

                        j.is_sent=True
                        j.save()
                    except:
                        j.is_sent=False
                        j.save()

