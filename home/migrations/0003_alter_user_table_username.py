# Generated by Django 4.2.7 on 2024-07-23 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_rename_password_user_table_password1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_table',
            name='username',
            field=models.CharField(max_length=100),
        ),
    ]
