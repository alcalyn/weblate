# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-09 12:00
from __future__ import unicode_literals

from django.db import migrations

from weblate.addons.models import ADDONS


FORMATS = {
    'po-unwrapped': 'po',
    'po-mono-unwrapped': 'po-mono',
}
NAME = 'weblate.gettext.customize'


def install_unwrapped_po(apps, schema_editor):
    """Install addons as replacement for hooks or flags."""
    SubProject = apps.get_model('trans', 'SubProject')
    Addon = apps.get_model('addons', 'Addon')
    Event = apps.get_model('addons', 'Event')

    for component in SubProject.objects.filter(file_format__in=FORMATS.keys()):
        addon = Addon.objects.get_or_create(
            component=component,
            name=NAME,
            defaults={
                'configuration': {'width': '-1'},
            }
        )[0]
        for event in ADDONS[NAME].events:
            Event.objects.get_or_create(
                addon=addon,
                event=event,
            )
        component.file_format = FORMATS[component.file_format]
        component.save()


class Migration(migrations.Migration):

    dependencies = [
        ('addons', '0004_auto_20180309_1300'),
    ]

    operations = [
        migrations.RunPython(install_unwrapped_po, reverse_code=install_unwrapped_po),
    ]