from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class MutsaUserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, nickname,password=None):
        if not nickname:
            raise ValueError('User must have a nickname')
        
        user = self.model(
            nickname=nickname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, nickname, password=None):
        user = self.create_user(
            nickname,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MutsaUser(AbstractBaseUser):
    nickname = models.CharField(max_length=255, unique=True)
    user_name = models.CharField(max_length=100, blank=True) #사용자로부터 받는 닉네임
    profile = models.ImageField(upload_to='profiles/', blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    refresh_token = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    school = models.CharField(max_length=30, blank=True)
    college = models.CharField(max_length=30, blank=True)


    objects = MutsaUserManager()

    USERNAME_FIELD = 'nickname'

    @property
    def is_staff(self):
        return self.is_admin



# Create your models here.
