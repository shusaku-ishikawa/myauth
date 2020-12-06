from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.core.validators import (
    RegexValidator, MaxValueValidator, MinValueValidator
)
from django.utils import timezone
class UserManager(BaseUserManager):
    """ユーザーマネージャー."""
    
    use_in_migrations = True

    def _create_user(self, user_id, password, **extra_fields):
        if not user_id:
            raise ValueError('The given user_id must be set')
        
        user = self.model(user_id = user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_id, password=None, **extra_fields):
        """is_staff(管理サイトにログインできるか)と、is_superuer(全ての権限)をFalseに"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_id, password, **extra_fields)

    def create_superuser(self, user_id, password, **extra_fields):
        """スーパーユーザーは、is_staffとis_superuserをTrueに"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(user_id, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
        カスタムユーザ
    """
    def __str__(self):
        return self.user_id
    user_id = models.CharField(verbose_name = 'ユーザID', max_length = 10, primary_key = True)
    family_name = models.CharField(verbose_name = '姓', max_length = 50)
    first_name = models.CharField(verbose_name = '名', max_length = 50)
    zip = models.CharField(
        verbose_name = '郵便番号',
        max_length = 10,
        validators = [
            RegexValidator(
                regex = '\d{3}\-?\d{4}',
                message = 'フォーマットが不正です。',
            )
        ]
    )
    address = models.CharField(verbose_name = '住所', max_length = 255)
    phone = models.CharField(
        verbose_name = '電話番号',
        max_length = 20,
        validators = [
            RegexValidator(
                regex = '[0-9\-\+]+',
                message = 'フォーマットが不正です。'
            )
        ]
    )
    unnamed1 = models.IntegerField(
        null = True,
        blank = True,
        verbose_name = '名称1',
        validators = [
            MaxValueValidator(9999999999),
            MinValueValidator(0),
        ]
    )
    unnamed2 = models.IntegerField(
        null = True,
        blank = True,
        verbose_name = '名称2',
        validators = [
            MaxValueValidator(9999),
            MinValueValidator(1000),
        ]
    )
    unnamed3 = models.IntegerField(
        null = True,
        blank = True,
        verbose_name = '名称3',
        validators = [
            MaxValueValidator(9999),
            MinValueValidator(1000),
        ]
    )
    unnamed4 = models.CharField(
        null = True,
        blank = True,
        verbose_name = '名称4',
        max_length = 10,
        validators = [
            RegexValidator(
                regex = '[0-9a-zA-Z]{1:10}'
            ),
        ]
    )
    date_joined = models.DateTimeField(verbose_name = '登録日', default = timezone.now)
    is_staff = models.BooleanField(
        _('管理者'),
        default=False,
        help_text=_(
        'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('利用開始'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'user_id'
    objects = UserManager()
    REQUIRED_FIELDS = [
        'family_name',
        'first_name',
        'zip',
        'address',
        'phone'
    ]