# Generated by Django 2.2 on 2020-02-26 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg', '0001_initial'),
        ('cms', '0006_actiontype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField()),
                ('follow_up', models.BooleanField(default=False)),
                ('follow_up_days', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_of_action', to='cms.ActionType')),
                ('claim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_claim', to='cms.Claim')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_user', to='login_reg.User')),
            ],
        ),
    ]
