# Generated by Django 4.2.2 on 2023-07-08 04:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phone_cases', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='phonecase',
            old_name='case_scaffold_img_path',
            new_name='case_scaffold_img',
        ),
    ]
