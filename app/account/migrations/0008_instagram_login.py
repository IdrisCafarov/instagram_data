# Generated by Django 3.2.18 on 2023-04-13 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_remove_instagram_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagram',
            name='login',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
