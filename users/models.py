from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    phone_number = PhoneNumberField(unique=True, verbose_name=_('Phone Number'))
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name=_('Profile Image'))
    full_name = models.CharField(max_length=255, verbose_name=_('Full Name'))
    coins = models.PositiveIntegerField(default=0, verbose_name=_('Coins'))
    telegram_id = models.CharField(max_length=50, verbose_name=_('Telegram ID'), unique=True)
    is_admin = models.BooleanField(default=False, verbose_name=_('Is Admin'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Is Staff'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))


    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['telegram_id']

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone_number)
