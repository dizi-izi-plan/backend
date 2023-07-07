# Generated by Django 3.2.19 on 2023-07-07 02:33

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PossibleActions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Возможные действия')),
            ],
            options={
                'verbose_name': 'Возможные действия',
                'verbose_name_plural': 'Возможные действия',
            },
        ),
        migrations.CreateModel(
            name='PossibleActionsTariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_tariff', to='info.possibleactions', verbose_name='Действия')),
            ],
            options={
                'verbose_name': 'Возможности тарифа',
                'verbose_name_plural': 'Возможности тарифа',
            },
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Наименование тарифа')),
                ('name_english', models.CharField(max_length=256, unique=True, verbose_name='Наименование тарифа на английском языке')),
                ('description', models.TextField(verbose_name='Описание тарифа')),
                ('cost', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0, message='Тариф должен быть больше 0 руб в мес')], verbose_name='Стоимость')),
                ('period', models.DurationField(choices=[(datetime.timedelta(days=30), 'месяц'), (datetime.timedelta(days=90), '3 месяца'), (datetime.timedelta(days=180), '6 месяцев'), (datetime.timedelta(days=270), '9 месяцев'), (datetime.timedelta(days=365), 'год')], default=datetime.timedelta(days=365), help_text='Выберите период действия', verbose_name='Период действия тарифа')),
                ('actions', models.ManyToManyField(related_name='tariff', through='info.PossibleActionsTariff', to='info.PossibleActions', verbose_name='Действия')),
            ],
            options={
                'verbose_name': 'Тариф',
                'verbose_name_plural': 'Тарифы',
            },
        ),
        migrations.CreateModel(
            name='UsersTariffs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата начала')),
                ('tariff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tariff', to='info.tariff', verbose_name='Тариф Пользователя')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_tariff', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Пользователь: Тариф',
                'verbose_name_plural': 'Пользователи: Тарифы',
            },
        ),
        migrations.AddField(
            model_name='possibleactionstariff',
            name='tariff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_tariff', to='info.tariff'),
        ),
        migrations.AddConstraint(
            model_name='possibleactionstariff',
            constraint=models.UniqueConstraint(fields=('action', 'tariff'), name='double_actions'),
        ),
    ]
