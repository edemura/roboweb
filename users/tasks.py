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
from users.models import Incomejson, TaskJson, Robo7Task
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
    
    
@app.task(ignore_result=True)
def make_robo7Task():
    for i in TaskJson.objects.exclude(is_task_set=True):
        try:
            task=Robo7Task
            task.patient_fio=i.last_name+' '+i.first_name+' '+i.middle_name
            task.analysis=i.analysis_name
            task.code=i.barcode
            task.create_datetime=datetime.now()
            task.save()
            i.is_task_set=True
            i.save()
        except:
            i.is_task_set=False
            i.save() 

        '''
        if i.is_processed==True:
            i.is_task_set=True
            i.save()
            
        else:
            i.is_task_set=False
            i.save()    
            '''