# Generated by Django 2.0.2 on 2018-03-11 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_estadistica'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_text', models.CharField(max_length=200)),
            ],
        ),
    ]
