# Generated by Django 4.2.5 on 2023-10-26 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0007_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amt',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
