from django.db import models
from django.conf import settings
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class People(models.Model):
    '''база данных физических лиц'''
    fio_sname = models.CharField(max_length=80, verbose_name="Фамилия")
    fio_name = models.CharField(max_length=80, verbose_name="Имя")
    fio_lname = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    dolznost = models.CharField(max_length=3, blank=False, null=True, choices=[('rn','Руководитель направления'),
                                            ('vi','Ведущий инженер'),
                                            ('1к','Инженер 1-й категории'),
                                            ('nah','Начальник отдела')], verbose_name='Должность')
    napravlenie = models.CharField(max_length=3, blank=True, null=True, choices=[('tee','Транспорт электроэнергии'),
                                            ('krp','Контроль режимов потребления'),
                                            ('ptp','Подготовка технических приложений к договорам энергоснабжения'),], verbose_name='Направление')
    #контактные данные
    cont_tel = PhoneNumberField(region='RU', blank=False, unique=True, verbose_name="Телефон")
    #id телеги
    id_telegramm = models.IntegerField(verbose_name="ID в телеграмме", blank=True, null=True)

    def __str__(self):
        return self.fio_sname

class Tempa(models.Model):
    '''база данных температуры'''
    sname = models.ForeignKey(People, blank=False, null=True, related_name='s_name', on_delete=models.RESTRICT, verbose_name='Сотрудник')
    temp = models.FloatField(blank=False, null=True, verbose_name="Температура")
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.sname.fio_sname+" - "+str(self.temp)

class Kalendar(models.Model):
    name = models.ForeignKey(People, blank=False, null=True, related_name='sotr_name', on_delete=models.RESTRICT, verbose_name='Сотрудник')
    day = models.DateField(blank=False, null=True, verbose_name='Дата начала')
    day_end = models.DateField(blank=False, null=True, verbose_name='Дата окончания')
    type = models.CharField(max_length=3, blank=False, null=True, choices=[('отп','Отпуск'),
                                                                           ('отг','Отгул'),
                                                                           ('раб','Рабочий день по приказу')],
                            verbose_name='Тип дня')
    comment = models.TextField(max_length=50, blank=True, null=False, verbose_name='Коментарий')
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.day)+' '+self.name.fio_sname+' - '+self.type

class Vakcina(models.Model):
    name = models.ForeignKey(People, blank=False, null=True, related_name='sotr_cert_name', on_delete=models.RESTRICT,
                             verbose_name='Сотрудник')
    etap_1 = models.DateField(blank=True, null=True, verbose_name='1-й этап вакцины')
    etap_2 = models.DateField(blank=True, null=True, verbose_name='2-й этап вакцины')
    medotvod = models.DateField(blank=True, null=True, verbose_name='Медотвод')
    covid_cert = models.DateField(blank=True, null=True, verbose_name='Сертификат переболевшего COVID')
    bl_covid = models.DateField(blank=True, null=True, verbose_name='Болеет COVID')
    srok_deystvia = models.DateField(blank=True, null=True, verbose_name='Срок действия сертификата/медотвода')
    cert = models.FileField(blank=True, verbose_name='Сертификат')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания записи')
    published_date = models.DateTimeField(default=timezone.now, verbose_name='Дата изменения записи')

    def __str__(self):
        return str(self.srok_deystvia)+' '+self.name.fio_sname

    def publish(self):
        self.published_date = timezone.now()
        self.save()


class Coffee(models.Model):
    name = models.ForeignKey(People, blank=False, null=True, related_name='coffee_sotr_name', on_delete=models.RESTRICT, verbose_name='Сотрудник')
    lastday = models.DateField(blank=False, null=True, verbose_name='Дата последнего дежурства')
    kolvo = models.IntegerField(blank=False, null=True, verbose_name='Количество отдежуренных дней')
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.day)+' '+self.name.fio_sname+' - '+self.type