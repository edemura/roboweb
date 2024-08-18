import json
import logging
from django.views import View
from django.http import JsonResponse
from telegram import Update

from dtb.celery import app
from dtb.settings import DEBUG
from tgbot.dispatcher import dispatcher
from tgbot.main import bot

from users.models import Incomejson
from django.core import serializers

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    dispatcher.process_update(update)


def index(request):
    return JsonResponse({"error": "sup hacker"})


class TelegramBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again.
    # Can be fixed with async celery task execution
    def post(self, request, *args, **kwargs):
        if DEBUG:
            process_telegram_event(json.loads(request.body))
        else:
            # Process Telegram event in Celery worker (async)
            # Don't forget to run it and & Redis (message broker for Celery)!
            # Locally, You can run all of these services via docker-compose.yml
            process_telegram_event.delay(json.loads(request.body))

        # e.g. remove buttons, typing event
        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request received! But nothing done"})

#добавлено мной

from json import loads
def recieve_json(request):
    if request.method == 'POST':
        #print(loads(request.body)['name'])
        json=Incomejson()
        #logger.info(request.body)
        #print("Goodbye cruel world!", file="stderr.txt")
        #data = serializers.serialize("json", request.body)
        json.text=request.body
        json.save()
        #json.process()

    return JsonResponse({"ok": "JSON received"})

#DRF

from users.models import Incomejson
from rest_framework import permissions, viewsets

from users.serializers import IncomeJsonSerializer, UserSerializer


class InconeJsonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Incomejson.objects.all().order_by('-create_datetime')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


