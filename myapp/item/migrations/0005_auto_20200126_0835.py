# Generated by Django 2.2.4 on 2020-01-25 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_auto_20200123_2304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='monthlySales',
            new_name='monthly_sales',
        ),
        migrations.AlterField(
            model_name='item',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female'), ('all', 'all')], default='all', max_length=10),
        ),
    ]