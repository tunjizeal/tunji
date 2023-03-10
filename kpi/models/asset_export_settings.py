# coding: utf-8
from django.db import models
from django.utils import timezone

from kpi.fields import KpiUidField


class AssetExportSettings(models.Model):
    """
    For a description of `export_settings`, see docstring of
    kpi.views.v2.asset_export_settings.AssetExportSettingsViewSet
    """
    uid = KpiUidField(uid_prefix='es')
    asset = models.ForeignKey('Asset', related_name='asset_export_settings',
                              on_delete=models.CASCADE)
    date_modified = models.DateTimeField()
    name = models.CharField(max_length=255, blank=True, default='')
    export_settings = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        self.date_modified = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_modified']
        unique_together = ('asset', 'name')

    def __str__(self):
        return f'{self.name} ({self.uid})'
