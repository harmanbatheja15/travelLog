# Generated by Django 3.1.3 on 2022-03-20 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myWebsite', '0003_auto_20220318_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='image',
            field=models.FileField(upload_to='travelImages'),
        ),
    ]