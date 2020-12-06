# Generated by Django 3.1.4 on 2020-12-05 05:11

import django.core.validators
from django.db import migrations, models
import myauth.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='ユーザID')),
                ('family_name', models.CharField(max_length=50, verbose_name='姓')),
                ('first_name', models.CharField(max_length=50, verbose_name='名')),
                ('zip', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='フォーマットが不正です。', regex='\\d{3}\\-?\\d{4}')], verbose_name='郵便番号')),
                ('address', models.CharField(max_length=255, verbose_name='住所')),
                ('phone', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='フォーマットが不正です。', regex='[0-9\\-\\+]+')], verbose_name='電話番号')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='管理者')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='利用開始')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', myauth.models.UserManager()),
            ],
        ),
    ]
