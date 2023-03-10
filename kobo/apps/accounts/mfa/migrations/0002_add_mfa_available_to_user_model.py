# Generated by Django 2.2.27 on 2022-07-05 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mfa', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kobomfamethod',
            options={'verbose_name': 'MFA Method', 'verbose_name_plural': 'MFA Methods'},
        ),
        migrations.CreateModel(
            name='MfaAvailableToUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'per-user availability',
                'verbose_name_plural': 'per-user availabilities',
            },
        ),
    ]
