from django.contrib import admin
from iiwork.models import Mpri, Spr_name_to, Tochki_ishodnik
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.

# @admin.register(Mpri)
# class MpriAdmin(admin.ModelAdmin):
#     list_display = ('id_tu', 'num_pu', 'mpri', 'active', 'neproveryat', )

# класс обработки данных
class MpriResource(resources.ModelResource):

    class Meta:
        model = Mpri

class Spr_name_toResource(resources.ModelResource):

    class Meta:
        model = Spr_name_to

class Tochki_ishodnikResource(resources.ModelResource):

    class Meta:
        model = Tochki_ishodnik

# вывод данных на странице
class MpriAdmin(ImportExportModelAdmin):
    resource_classes = [MpriResource]

class Spr_name_toAdmin(ImportExportModelAdmin):
    resource_classes = [Spr_name_toResource]

class Tochki_ishodnikAdmin(ImportExportModelAdmin):
    resource_classes = [Tochki_ishodnikResource]

admin.site.register(Mpri, MpriAdmin)
admin.site.register(Spr_name_to, Spr_name_toAdmin)
admin.site.register(Tochki_ishodnik, Tochki_ishodnikAdmin)

#Spr_name_to, Tochki_ishodnik, Spr_name_toAdmin, Tochki_ishodnikAdmin