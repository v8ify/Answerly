# Generated by Django 3.1.1 on 2021-03-10 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210308_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='content_markdown',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]
