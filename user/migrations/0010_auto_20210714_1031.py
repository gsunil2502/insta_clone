# Generated by Django 3.1.3 on 2021-07-14 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20210714_0956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_private_account',
        ),
        migrations.AddField(
            model_name='user',
            name='account',
            field=models.CharField(choices=[('private', 'PRIVATE'), ('public', 'PUBLIC')], default='private', max_length=10),
        ),
    ]
