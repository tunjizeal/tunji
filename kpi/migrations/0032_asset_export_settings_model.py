# Generated by Django 2.2.7 on 2021-03-04 20:53

import django.db.models.deletion
from django.db import migrations, models

import kpi.fields.kpi_uid


class Migration(migrations.Migration):

    dependencies = [
        ('kpi', '0031_remove_objectpermission_generic_relation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asset',
            options={'default_permissions': ('add', 'change', 'delete'), 'ordering': ['-date_modified'], 'permissions': (('view_asset', 'Can view asset'), ('discover_asset', 'Can discover asset in public lists'), ('manage_asset', 'Can manage all aspects of asset'), ('add_submissions', 'Can submit data to asset'), ('view_submissions', 'Can view submitted data for asset'), ('partial_submissions', 'Can make partial actions on submitted data for asset for specific users'), ('change_submissions', 'Can modify submitted data for asset'), ('delete_submissions', 'Can delete submitted data for asset'), ('validate_submissions', 'Can validate submitted data asset'), ('from_kc_only', 'INTERNAL USE ONLY; DO NOT ASSIGN'))},
        ),
        migrations.CreateModel(
            name='AssetExportSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', kpi.fields.kpi_uid.KpiUidField(uid_prefix='es')),
                ('date_modified', models.DateTimeField()),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('export_settings', models.JSONField(default=dict)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asset_export_settings', to='kpi.Asset')),
            ],
            options={
                'ordering': ['-date_modified'],
                'unique_together': {('asset', 'name')},
            },
        ),
    ]
