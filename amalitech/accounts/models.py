from django.db import models
from django.contrib.auth.models import AbstractUser

class FileServerUser(AbstractUser):
    is_admin = models.BooleanField(default=False)

    # Modify related_name for each field to ensure they are unique
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="fileserveruser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="fileserveruser_set",
        related_query_name="user",
    )

    def __str__(self):
        # Fix the string conversion of is_admin to ensure it works correctly
        stin = f'{self.username}, {self.email}, {"Admin" if self.is_admin else "Not Admin"}'
        return stin
