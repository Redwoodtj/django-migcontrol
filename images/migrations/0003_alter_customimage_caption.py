# Generated by Django 3.2.13 on 2022-07-13 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_migrate_old_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customimage',
            name='caption',
            field=models.CharField(blank=True, max_length=5096),
        ),
    ]