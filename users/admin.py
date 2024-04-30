from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from dtb.settings import DEBUG

from users.models import Location
from users.models import User, Robo7Task
from users.forms import BroadcastForm

from users.tasks import broadcast_message
from tgbot.handlers.broadcast_message.utils import send_one_message


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'username', 'first_name', 'last_name', 
        'language_code', 'deep_link',
        'created_at', 'updated_at', "is_blocked_bot",
    ]
    list_filter = ["is_blocked_bot", ]
    search_fields = ('username', 'user_id')

    actions = ['broadcast']

    def broadcast(self, request, queryset):
        """ Select users via check mark in django-admin panel, then select "Broadcast" to send message"""
        user_ids = queryset.values_list('user_id', flat=True).distinct().iterator()
        if 'apply' in request.POST:
            broadcast_message_text = request.POST["broadcast_text"]

            if DEBUG:  # for test / debug purposes - run in same thread
                for user_id in user_ids:
                    send_one_message(
                        user_id=user_id,
                        text=broadcast_message_text,
                    )
                self.message_user(request, f"Just broadcasted to {len(queryset)} users")
            else:
                broadcast_message.delay(text=broadcast_message_text, user_ids=list(user_ids))
                self.message_user(request, f"Broadcasting of {len(queryset)} messages has been started")

            return HttpResponseRedirect(request.get_full_path())
        else:
            form = BroadcastForm(initial={'_selected_action': user_ids})
            return render(
                request, "admin/broadcast_message.html", {'form': form, 'title': u'Broadcast message'}
            )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'created_at']


#Все что ниже самописное для робо7

class Robo7TaskAdmin(admin.ModelAdmin):
    list_display=['patient_fio', 'analysis', 'code', 'tray_num', 'is_tray_assigned',
                  'is_validated', 'filename', 'is_filename', 'label', 'is_label', 'is_sent', 'is_complete', 'create_datetime', 'update_datetime', 'filenameok','tray_num_task',]
    fieldsets = [
        (None, {"fields": ['patient_fio', 'analysis', 'code', 'tray_num', 'is_tray_assigned',
                  'is_validated', 'filename', 'is_filename', 'label', 'is_label', 'is_sent', 'is_complete', 'create_datetime', 'update_datetime','filenameok','tray_num_task',]}),
        
    ]
  
admin.site.register(Robo7Task, Robo7TaskAdmin) 