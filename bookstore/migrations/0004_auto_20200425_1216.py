# Generated by Django 3.0.2 on 2020-04-25 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0003_auto_20200417_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_status',
            field=models.CharField(choices=[('Unavailable', 'Unavailable'), ('Available', 'Available')], max_length=45),
        ),
    ]
