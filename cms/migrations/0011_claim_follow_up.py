# Generated by Django 2.2 on 2020-02-28 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0010_auto_20200227_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='follow_up',
            field=models.BooleanField(default=False),
        ),
    ]
