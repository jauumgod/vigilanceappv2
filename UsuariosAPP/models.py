# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# class UserManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):
#         if not username:
#             raise ValueError('O campo username é obrigatório')
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser precisa ter is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser precisa ter is_superuser=True.')

#         return self.create_user(username, password, **extra_fields)


# class Usuarios(AbstractBaseUser):
#     username = models.CharField(max_length=255, unique=True)
#     email = models.EmailField(unique=True, blank=True, null=True)
#     cpf = models.CharField(max_length=255, blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)


#     objects = UserManager()
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     def __str__(self):
#         return self.username

#     def has_perm(self, perm, obj=None):
#         return self.is_superuser

#     def has_module_perms(self, app_label):
#         return self.is_superuser