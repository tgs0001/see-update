# Generated by Django 5.0.6 on 2024-06-03 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rate_employees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluateeid', models.IntegerField()),
                ('evaluatorid', models.IntegerField()),
                ('secDeptEv', models.IntegerField(default=None)),
                ('commEv', models.IntegerField(default=None)),
                ('behavEv', models.IntegerField(default=None)),
                ('comid', models.IntegerField(default=None)),
            ],
        ),
    ]
