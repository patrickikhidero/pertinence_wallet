# Generated by Django 4.0 on 2022-01-07 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=128)),
                ('type', models.CharField(choices=[('payment_received', 'payment_received'), ('payment_made', 'payment_made'), ('payment_withdraw', 'payment_withdraw'), ('payment_fill', 'payment_fill')], default='payment_made', max_length=64)),
                ('date', models.DateField(auto_now_add=True, verbose_name='Dates')),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
            ],
        ),
    ]
