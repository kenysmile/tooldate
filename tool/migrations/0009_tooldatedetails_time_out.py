# Generated by Django 4.0.6 on 2022-07-10 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0008_alter_tooldatedetails_extra_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='tooldatedetails',
            name='time_out',
            field=models.FloatField(default='1'),
            preserve_default=False,
        ),
    ]
