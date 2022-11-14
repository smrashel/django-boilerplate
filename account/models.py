from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    contact_number = models.CharField('Contact Number', max_length = 200, unique = True)
    employee_id = models.CharField('Employee ID', max_length = 200, unique = True)
    image = models.ImageField(verbose_name='Image', upload_to='images/', null=True, blank=True)

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['id']

    def __str__(self):
        return self.employee_id