# Generated by Django 3.2.6 on 2021-08-06 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytbot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='dolznost',
            field=models.CharField(choices=[('rn', 'Руководитель направления'), ('vi', 'Ведущий инженер'), ('1к', 'Инженер 1-й категории'), ('nah', 'Начальник отдела')], max_length=3, null=True, verbose_name='Должность'),
        ),
    ]
