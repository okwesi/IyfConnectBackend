import random
import datetime
from asgiref.sync import sync_to_async
from django.contrib.auth.models import Permission, UserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser, Group
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone

from apps.shared.models import BaseModel
from apps.shared.utils.validators import validate_only_digits
from apps.shared.overrides import FileNameEngine


class PermissionManager(models.Manager):
    def get_permissions(self, *args, **kwargs):
        """
        Custom manager method to get filtered permissions.
        """
        return super().get_queryset().exclude(
            Q(codename__startswith='add_') |
            Q(codename__startswith='change_') |
            Q(codename__startswith='delete_') |
            Q(codename__startswith='view_')
        )


class AppPermission(Permission):
    """
    Proxy model to attach the custom manager to the built-in Permission model.
    """
    objects = PermissionManager()

    class Meta:
        proxy = True


class GroupManager(models.Manager):
    def get_groups(self, is_active=False, *args, **kwargs):
        """
        Custom manager method to get filtered groups.
        """
        if is_active:
            return Group.objects.filter(ranking__is_active=True)
        return Group.objects.all()

    def get_super_admin_group(self, *args, **kwargs):
        return self.get(ranking__is_default=True, name='Super Admin')


class AppGroup(Group):
    """
    Proxy model to attach the custom manager to the built-in group model.
    """
    objects = GroupManager()

    class Meta:
        proxy = True


class CustomUserManager(UserManager):
    """
    Custom manager for User model to add additional methods.
    """

    def get_users_with_permission(self, permission):
        """
        Retrieve all users who have a given permission or are superusers.

        Args:
            permission (str): The codename of the permission to check.

        Returns:
            QuerySet: A queryset of User instances that have the specified permission or are superusers.
        """
        # Get the permission object
        try:
            permission = Permission.objects.get(codename=permission)
        except Permission.DoesNotExist:
            # Handle the case where the permission does not exist
            return self.none()

        # Query for users with the permission directly, through a group, or who are superusers
        return self.get_queryset().filter(
            Q(user_permissions=permission) |
            Q(groups__permissions=permission) | Q(is_superuser=True)
        ).distinct()


class User(AbstractUser, BaseModel, PermissionsMixin):
    GENDER_CHOICES = (
        ('m', 'Male'), 
        ('f', 'Female')
    )
    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=10, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True, max_length=40, blank=False, null=True,
                                    validators=[
                                        MinLengthValidator(
                                            12, "Phone number number must be at least 14 characters."),
                                        validate_only_digits], )
    avatar = models.ImageField(upload_to=FileNameEngine('avatars/'), null=True, blank=True)
    verification_code = models.IntegerField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    date_verified = models.DateTimeField(blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    objects = CustomUserManager()

    class Meta:
        permissions = [
            # users:
        ]

    def set_email_verification(self):
        self.verification_code = random.randint(10000, 99999)
        self.save()
        return self.verification_code

    def set_is_verified(self):
        self.is_verified = True
        self.verified_on = timezone.now()
        self.save()

 
    @property
    def is_super_admin(self):
        return self.groups.filter(name='Super Admin', ranking__is_default=True).exists()

    def __str__(self):
        return f'{self.id}-{self.get_full_name()}'


class GroupRank(BaseModel):
    group = models.OneToOneField(
        Group, on_delete=models.CASCADE, related_name='ranking')
    rank = models.PositiveIntegerField()
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.group.name} - {self.rank}'

    class Meta:
        ordering = ['rank']
