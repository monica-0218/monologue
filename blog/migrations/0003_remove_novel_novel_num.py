# Generated by Django 3.0.6 on 2020-05-12 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200512_2151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novel',
            name='novel_num',
        ),
    ]
