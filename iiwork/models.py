from django.db import models
from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Mpri(models.Model):
    tu_id = models.CharField(max_length=10, verbose_name="ID ТУ")
    pu_num = models.CharField(max_length=64, verbose_name="Номер ПУ")
    mpri = models.IntegerField(verbose_name="Межпроверочный интервал, дней", blank=False, null=False)
    created_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(verbose_name="МПРИ активен", default=True, blank=False, null=False)
    neproveryat = models.BooleanField(verbose_name="Не проверять", default=False, blank=False, null=False)

    def __str__(self):
        return self.tu_id +" - "+self.pu_num

    def publish(self):
        self.created_date = timezone.now()
        self.save()

class Spr_name_to(models.Model):
    name_to = models.CharField(max_length=128, verbose_name="Натименование ТО")

    def __str__(self):
        return self.name_to


class Tochki_ishodnik(models.Model):

    potreb_name = models.CharField(max_length=256, verbose_name="Наименование потребителя")
    dog_num = models.CharField(max_length=14, verbose_name="Номер договора")
    dogovornoe_podrazdelenie = models.ForeignKey(Spr_name_to, blank=False, null=True, related_name='name_to_dog',
                                                 on_delete=models.RESTRICT,
                                                 verbose_name='Договорное подразделение')
    oesk_class = models.CharField(max_length=128, verbose_name="Признак по классификатору ОЭСК")
    eo_num  = models.CharField(max_length=18, verbose_name="Номер энергообъекта")
    eo_name = models.CharField(max_length=512, verbose_name="Наименование энергообъекта")
    eo_id = models.CharField(max_length=10, verbose_name="ID ЭО")
    tp_id = models.CharField(max_length=10, verbose_name="ID ТП")
    grbp = models.CharField(max_length=512, verbose_name="Место (точка) РБП")
    so = models.CharField(max_length=128, verbose_name="Сетевая организация (ТП)")
    tu_id = models.CharField(max_length=10, verbose_name="ID ТУ")
    tu_name = models.CharField(max_length=512, verbose_name="Наименование ТУ")
    tu_power = models.FloatField(verbose_name='Мощность ТУ')
    tu_tr_netr = models.CharField(max_length=3, blank=False, null=True,
                                  choices=[('Тра','Транзитная ТУ'), ('Нет','Не транзитная ТУ')],
                                  verbose_name='Транзитная-нетранзитная ТУ')
    ik_priemnik = models.CharField(max_length=128, verbose_name="ИК приемник")
    razmeshenie = models.CharField(max_length=512, verbose_name="Размещение")
    tu_1_power = models.FloatField(verbose_name='Мощность ТУ 1')
    pu_num = models.CharField(max_length=64, verbose_name="Номер ПУ")
    tp_name = models.CharField(max_length=512, verbose_name="Наименование ТП")
    tu_starshaya = models.IntegerField(verbose_name='Старшая ТУ')
    pu_type = models.CharField(max_length=128, verbose_name="Тип ПУ")
    pu_mpi = models.IntegerField(verbose_name='МПИ')
    pu_poverka_date = models.CharField(max_length=10, verbose_name='Дата поверки')
    eo_state = models.CharField(max_length=2, blank=False, null=True,
                                choices=[('Ак','Активен'), ('Зк','Закрыт'), ('НО','Не определено'),('Н','Новый')],
                                verbose_name='Транзитная-нетранзитная ТУ')
    tu_num = models.IntegerField(verbose_name='Номер ТУ')
    ck = models.IntegerField(verbose_name='ЦК', blank=True, null=True)
    ppn_category = models.CharField(max_length=128, verbose_name="Категория ППН")
    tarif_name = models.CharField(max_length=128, verbose_name="Наименование тарифа")
    tranzit_golova_tu = models.CharField(max_length=64, verbose_name="Номер транзитной ТУ на голове")
    tranzit_golova_eo = models.CharField(max_length=18, verbose_name="Номер энергообъекта головного потребителя")
    tranzit_golova_tu = models.IntegerField(verbose_name='Номер ТУ головного потребителя')

    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.potreb_name + " - " + self.tu_id

    def publish(self):
        self.created_date = timezone.now()
        self.save()

class Data_proverki_ii(models.Model):
    id_tu = models.CharField(max_length=10, verbose_name="ID ТУ")
    num_pu = models.CharField(max_length=64, verbose_name="Номер ПУ")
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id_tu + " - " + self.num_pu

    def publish(self):
        self.created_date = timezone.now()
        self.save()
