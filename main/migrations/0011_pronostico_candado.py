# Generated by Django 2.0.2 on 2018-03-03 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20180302_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='pronostico',
            name='candado',
            field=models.BooleanField(default=False),
        ),
    ]
