# Generated by Django 3.1.3 on 2022-03-22 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myWebsite', '0008_auto_20220323_0446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logimage',
            name='image',
            field=models.ImageField(upload_to='travelImages/'),
        ),
    ]
