# Generated by Django 3.1.3 on 2021-06-26 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210625_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, help_text="Provide your personal information, even if the account is used for a business, a pet or something else. This won't be a part of your public profile.", null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(help_text="Help people discover your account by using the name you're known by: either your full name, nickname, or business name.", max_length=100),
        ),
    ]
