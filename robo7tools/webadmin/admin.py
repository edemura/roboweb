from django.contrib import admin

# Register your models here.

from .models import Member, ConfigType, Config, TubeType, TrayTube, Analysis, AnalysisSet, Task, Robo7Task

# Register your models here.


     


class ConfigInline(admin.StackedInline):
    model = Config
    extra = 3


class ConfigTypeAdmin(admin.ModelAdmin):
    
    list_display = ["configtype"]
    fieldsets = [
        (None, {"fields": ["configtype"]}),
        
    ]
    inlines = [ConfigInline]

#admin.site.register(Member)
admin.site.register(ConfigType, ConfigTypeAdmin)

admin.site.register(TubeType)

class TrayTubeInline(admin.StackedInline):
    model = TrayTube
    extra = 3 

class AnalysisInline(admin.StackedInline):
    model = Analysis
    extra = 3 

class AnalysisSetAdmin(admin.ModelAdmin):
    
    list_display = ["set", "active"]
    fieldsets = [
        (None, {"fields": ["set", "active"]}),
        
    ]
    inlines = [AnalysisInline, TrayTubeInline]

admin.site.register(AnalysisSet, AnalysisSetAdmin)  

class TaskAdmin(admin.ModelAdmin):
    
    list_display = ["name","status","timeupdate",]
    fieldsets = [
        (None, {"fields": ["name","status","timeupdate", ]}),
        
    ]

#admin.site.register(Task, TaskAdmin) 

class Robo7TaskAdmin(admin.ModelAdmin):
    list_display=['patient_fio', 'analysis', 'code', 'tray_num', 'is_tray_assigned',
                  'is_validated', 'filename', 'is_filename', 'label', 'is_label', 'is_sent', 'is_complete', 'create_datetime', 'update_datetime', 'filenameok','tray_num_task',]
    fieldsets = [
        (None, {"fields": ['patient_fio', 'analysis', 'code', 'tray_num', 'is_tray_assigned',
                  'is_validated', 'filename', 'is_filename', 'label', 'is_label', 'is_sent', 'is_complete', 'create_datetime', 'update_datetime','filenameok','tray_num_task',]}),
        
    ]
  
admin.site.register(Robo7Task, Robo7TaskAdmin) 