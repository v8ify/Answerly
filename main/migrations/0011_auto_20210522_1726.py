# Generated by Django 3.1.1 on 2021-05-22 11:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0010_answerreport_questionreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answerreport',
            name='reporter',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='questionreport',
            name='reporter',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
