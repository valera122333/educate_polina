# Generated by Django 5.0.2 on 2024-02-14 02:46

import django.db.models.deletion
import users_app.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=500, verbose_name='О себе')),
                ('profile_pic', models.ImageField(default='images/23.webp', upload_to=users_app.models.path_and_rename, verbose_name='Изображение профиля')),
                ('user_type', models.CharField(choices=[('teacher', 'Наставник'), ('student', 'Студент')], default='student', max_length=30, verbose_name='Тип пользователя')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Информация о пользователях',
                'verbose_name_plural': 'Информация о пользователях',
            },
        ),
    ]