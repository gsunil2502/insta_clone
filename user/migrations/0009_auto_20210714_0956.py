# Generated by Django 3.1.3 on 2021-07-14 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20210713_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_private_account',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')]),
        ),
    ]
