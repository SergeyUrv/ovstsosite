from django.shortcuts import render
from django.http import JsonResponse
from .models import People, Tempa, Kalendar
import datetime

# Create your views here.

def get_temp(request):
    j = {}
    j['fio_temp'] = {}
    j['fio_prim'] = {}
    for p in People.objects.all():
        comment = ''
        try:
            #ищем последнюю внесенную температуру
            ptemp=Tempa.objects.filter(sname=p, created_date__gte=datetime.date.today()).order_by('-created_date')[:1].get().temp
        except Tempa.DoesNotExist:
            try:
                otgul = Kalendar.objects.filter(name=p, day__lte=datetime.date.today(),
                                                day_end__gte=datetime.date.today()).exclude(type__exact='раб').order_by(
                    '-created_date')[:1].get()
                ptemp = otgul.get_type_display()
                comment = otgul.comment
            except Kalendar.DoesNotExist:
                ptemp = '-'
        j['fio_temp'][str(p.fio_sname)] = str(ptemp)
        j['fio_prim'][str(p.fio_sname)] = str(comment)
    j['result'] = 'ok'
    return JsonResponse(j)