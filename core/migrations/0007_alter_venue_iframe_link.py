# Generated by Django 5.0.6 on 2024-05-27 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_venue_localization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='iframe_link',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
