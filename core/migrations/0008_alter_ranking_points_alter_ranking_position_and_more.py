# Generated by Django 5.0.6 on 2024-05-27 19:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_venue_iframe_link'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='ranking',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='position',
            field=models.IntegerField(blank=True, default=0, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]