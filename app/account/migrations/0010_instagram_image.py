# Generated by Django 3.2.18 on 2023-04-13 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_instagram_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagram',
            name='image',
            field=models.ImageField(null=True, upload_to='instagram_pp'),
        ),
    ]
