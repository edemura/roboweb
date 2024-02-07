from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)

#виды конфигураций
class ConfigType(models.Model):
  
  class Meta:
     verbose_name=_('Конфигурфция')
     verbose_name_plural=_('Конфигурации')
  configtype = models.CharField(max_length=255, verbose_name="Типы конфигураций")
  def __str__(self):
    return self.configtype
  
  def write(self): 

    with open(self.configtype,'w') as file:
        
        file.write(self.configtype)
        file.close()
    return self.configtype
  
# Конфигурации
class Config(models.Model):
  class Meta:
     verbose_name=_('Параметр')
     verbose_name_plural=_('Параметры')
  configtype = models.ForeignKey(
        "webadmin.ConfigType",
        on_delete=models.CASCADE,
        verbose_name="Типы конфигураций"
    )


  name = models.CharField(max_length=255)
  value = models.CharField(max_length=255, null=True)


  def write(self): 

    with open(self.name,'w') as file:
        
        file.write(self.value)
        file.close()
    return self.value
  
# Наборы исследований

class AnalysisSet(models.Model):
  
  class Meta:
     verbose_name=_('Набор исследования')
     verbose_name_plural=_('Наборы исследования')

  set = models.CharField(max_length=255, verbose_name="Наборы исследований")
  active = models.BooleanField(null=False, default=False, verbose_name="Активный набор")
  
  # def set_active(self, active):
  #   if active==True:
  #     for i in AnalysisSet.objects.all():
  #       i.__active=False
  #       i.save()
  #     self.active=True
  #   else:
  #      self.active=False

  # def get_active(self):
  #    return self.active

  # active=property(get_active, set_active)   

  def __str__(self):
    return self.set
  

# Типы пробирок

class TubeType(models.Model):

  class Meta:
     verbose_name=_('Тип пробирки')
     verbose_name_plural=_('Виды пробирок')
  
  volume = models.CharField(max_length=255, verbose_name="Объем")
  color = models.CharField(max_length=255, verbose_name="Цвет")
  filler = models.CharField(max_length=255, verbose_name="Наполнитель")
  def __str__(self):
    return self.volume+' '+self.color+' '+self.filler


# Пробирки в лотках

class TrayTube(models.Model):

  class Meta:
     verbose_name=_('Лоток')
     verbose_name_plural=_('Расположение видов пробирок в лотках')

  set = models.ForeignKey(
        "webadmin.AnalysisSet",
        on_delete=models.CASCADE,
        verbose_name="Набор исследований"
    )

  tube_type = models.ForeignKey(
        "webadmin.TubeType",
        on_delete=models.CASCADE,
        verbose_name="Тип пробирок"
    )
  
  tray = models.IntegerField(unique=True, verbose_name="Номер лотка")

  def __str__(self):
    return '#'+str(self.tray)

# Исследования        

class Analysis(models.Model):

  class Meta:
     verbose_name=_('Вид исследования')
     verbose_name_plural=_('Виды исследований')

  set = models.ForeignKey(
        "webadmin.AnalysisSet",
        on_delete=models.CASCADE,
        verbose_name="Набор исследований"
    )
  tube_type = models.ForeignKey(
      "webadmin.TubeType",
      on_delete=models.CASCADE,
      verbose_name="Тип пробирки"
  )
  analysis_name = models.CharField(max_length=255, verbose_name="Вид исследования")

  def __str__(self):
    return self.analysis_name
  
# Задачи
# перименовать в service
class Task(models.Model):
  name = models.CharField(max_length=255, verbose_name="Наименование задачи")
  RUNNING = 1
  STOPPED =2
  CRASHED =3
  STATUS_CHOICES = [
        (RUNNING, "Running"),
        (STOPPED, "Stopped"),
        (CRASHED, "Crashed"),
        
    ]
  status=models.IntegerField(verbose_name="Статус", choices=STATUS_CHOICES, default=2)
  timeupdate = models.DateTimeField(null=True)

  def __str__(self):
    return self.name
  
  def run(self):
    pass

  @property
  def value(self):
        return self._value

  @value.setter
  def value(self, x):
        print(f'value={x}')
        self._value = x

# История задачи

#Задачи robo7

class Robo7Task(models.Model):
  
  class Meta:
     verbose_name=_('Задание на приборе')
     verbose_name_plural=_('Задания на приборе')

  patient_fio = models.CharField(max_length=255, verbose_name="ФИО пациента")
  analysis = models.CharField(max_length=255, verbose_name="Наименование вида исследования")
  code = models.CharField(max_length=255, verbose_name="ШК")
  tray_num = models.IntegerField(null=True, default=0, verbose_name="Назначенный лоток")
  is_tray_assigned = models.BooleanField(null=True, default=None, verbose_name="Лоток назначен")
  is_validated = models.BooleanField(null=True, default=None, verbose_name="Валидация пройдена")
  is_sent = models.BooleanField(null=True, default=None, verbose_name="Отправлено на прибор")
  is_complete = models.BooleanField(null=True, default=None, verbose_name="Выполнено")
  is_filename = models.BooleanField(null=True, default=None, verbose_name="Сформировано имя файла")
  filename = models.CharField(max_length=255, null=True, default=None, verbose_name="Имя файла")
  filenameok = models.CharField(max_length=255, null=True, default=None, verbose_name="Имя файла OK")
  is_label = models.BooleanField(null=True, default=None, verbose_name="Сформировано содержание этикетки")
  label = models.CharField(max_length=255, null=True, default=None, verbose_name="Содержание этикетки")
  create_datetime = models.DateTimeField(null=True, auto_now=False, auto_now_add=True, verbose_name='Создано')
  update_datetime = models.DateTimeField(null=True, auto_now=True, auto_now_add=False, verbose_name='Изменено')
  tray_num_task = models.IntegerField(null=True, default=0, verbose_name="tray num за текущую дату")

  def __str__(self):
    return self.patient_fio+' '+self.code+' '+str(self.create_datetime)
  
  '''
  def __init__(self, *args: Any, **kwargs: Any) -> None:
    super().__init__(*args, **kwargs)
     
    #prev=Robo7Task.objects.get(pk=self.pk-1)
    #prev = Robo7Task.objects.filter(pk__lt=self.pk).order_by('create_datetime').first()
    prev = Robo7Task.objects.order_by('create_datetime')[0]
    if self.create_datetime.date==prev.create_datetime.date:
      self.tray_num_task=prev.tray_num_task+1
    else:
      self.tray_num_task=1
  
    self.tray_num_task=1
  
    self.save()
    '''    
  #  def __init__(self, *args: Any, **kwargs: Any) -> None:
  #     super().__init__(*args, **kwargs)

#имя файла конфигурация
class Filename:
    template='{terminal_host},{terminal_robo7},{date},{tray_number},{last_tube},{seq_tray},{queue},{patient_id},{patient_name},{container_name},{sample_volume},{department_name},{number_of_labels},{stocker_code},{rfid},{priority}'
    templateok='{terminal_host},{terminal_robo7},{date},{tray_number},OK'
    terminal_host='0005'
    terminal_robo7='0001'
    date='1213'
    #tray_number='0032'
    tray_number='0001'
    last_tube='9'
    seq_tray='01'
    queue='1234'
    patient_id='0123456789'
    patient_name='Ivan Petrov'
    container_name='HbA1c'
    sample_volume='1.0'
    department_name='Pediatrics'
    number_of_labels='1'
    stocker_code='01'
    rfid=''
    priority='0'
    

    def make(self):
       tmpl=self.template.format(terminal_host=self.terminal_host,
                                 terminal_robo7=self.terminal_robo7,
                                 date=self.date,
                                 tray_number=self.tray_number,
                                 last_tube=self.last_tube,
                                 seq_tray=self.seq_tray,
                                 queue=self.queue,
                                 patient_id=self.patient_id,
                                 patient_name=self.patient_name,
                                 container_name=self.container_name,
                                 sample_volume=self.sample_volume,
                                 department_name=self.department_name,
                                 number_of_labels=self.number_of_labels,
                                 stocker_code=self.stocker_code,
                                 rfid=self.rfid,
                                 priority=self.priority)
       
       return tmpl
    
    def makeok(self):
       tmpl=self.templateok.format(terminal_host=self.terminal_host,
                                 terminal_robo7=self.terminal_robo7,
                                 date=self.date,
                                 tray_number=self.tray_number,
                                 )
       
       return tmpl



class Label:
   template='BAR|{x_pos}^{y_pos}^{height}^{barcode_type}^{code_type}^{narrow_width}^{wide_width}^{check_digit}^{draw_direction}^{barcode_data}|CR'
   x_pos='2'
   y_pos='2'
   height='15'
   barcode_type='7'
   code_type='1'
   narrow_width='4'
   wide_width='8'
   check_digit='1'
   draw_direction='0'
   barcode_data='11111'

   def make(self):
      lbl=self.template.format(x_pos=self.x_pos,                         
            y_pos=self.y_pos,
            height=self.height,
            barcode_type=self.barcode_type,
            code_type=self.code_type,
            narrow_width=self.narrow_width,
            wide_width=self.wide_width,
            check_digit=self.check_digit,
            draw_direction=self.draw_direction,
            barcode_data=self.barcode_data)
      return lbl