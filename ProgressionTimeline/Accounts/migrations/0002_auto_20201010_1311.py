# Generated by Django 3.0.4 on 2020-10-10 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, default=None, max_length=256, null=True),
        ),
    ]
