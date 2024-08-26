"""
    Celery tasks. Some of them will be launched periodically from admin panel via django-celery-beat
"""

import time
from typing import Union, List, Optional, Dict

import telegram

from dtb.celery import app
from celery.utils.log import get_task_logger
from tgbot.handlers.broadcast_message.utils import send_one_message, from_celery_entities_to_entities, \
    from_celery_markup_to_markup

logger = get_task_logger(__name__)


@app.task(ignore_result=True)
def broadcast_message(
    user_ids: List[Union[str, int]],
    text: str,
    entities: Optional[List[Dict]] = None,
    reply_markup: Optional[List[List[Dict]]] = None,
    sleep_between: float = 0.4,
    parse_mode=telegram.ParseMode.HTML,
) -> None:
    """ It's used to broadcast message to big amount of users """
    logger.info(f"Going to send message: '{text}' to {len(user_ids)} users")

    entities_ = from_celery_entities_to_entities(entities)
    reply_markup_ = from_celery_markup_to_markup(reply_markup)
    for user_id in user_ids:
        try:
            send_one_message(
                user_id=user_id,
                text=text,
                entities=entities_,
                parse_mode=parse_mode,
                reply_markup=reply_markup_,
            )
            logger.info(f"Broadcast message was sent to {user_id}")
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}, reason: {e}")
        time.sleep(max(sleep_between, 0.1))

    logger.info("Broadcast finished!")


#мое
    
from celery import shared_task
from users.models import Incomejson, TaskJson, Robo7Task, Analysis, AnalysisSet, TrayTube
from time import sleep
from datetime import datetime

#@shared_task()
@app.task(ignore_result=True)
def make_true():
    for i in Incomejson.objects.all():
        if i.is_processed==True:
            i.is_task_set=True
            i.save()
            
        else:
            i.is_task_set=False
            i.save()
    
#Создание из JSON экземпляра типа задание для ROBO7   
@app.task(ignore_result=True)
def make_robo7Task():
    for i in TaskJson.objects.exclude(is_task_set=True):
        try:
            task=Robo7Task()
            task.patient_fio=i.last_name+' '+i.first_name+' '+i.middle_name
            task.analysis=i.analysis_name
            task.code=i.barcode
            task.create_datetime=datetime.now()
            task.save()
            i.is_task_set=True
            i.save()
        except Exception as e:
            i.is_task_set=False
            i.exception_text=f"Failed to make task {type(e)}, reason: {e}"
            i.save() 

#Присвоение заданиям номеров лотков, в которых находится подходящий тип пробирки
@app.task(ignore_result=True)
def tray_assign():
    for i in Robo7Task.objects.exclude(is_tray_assigned=True):
        try:
            an=Analysis.objects.filter(set=AnalysisSet.objects.get(active=True), analysis_name=i.analysis)
            tube_type=an[0].tube_type
            tray_tube=TrayTube.objects.filter(tube_type=tube_type)[0]
            if tray_tube!=None:
                i.tray_num=tray_tube.tray
                i.is_tray_assigned=True
            else:
                i.is_tray_assigned=False
                i.exception_text=f"Для вида исследования {i.analysis}, не найдено доступных видов пробирок"
            i.save()
        except Exception as e:
            i.is_tray_assigned=False
            i.exception_text=f"Failed to assign tray {type(e)}, reason: {e}"
            i.save()
