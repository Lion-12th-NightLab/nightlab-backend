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

# class ProfileChoices(models.TextChoices):
#     gentle = 'gentle', 'gentle' # 온화한 등대지기
#     serious = 'serious', 'serious' # 진지한 등대지기
#     sharp = 'sharp', 'sharp' # 까칠한 등대지기


class MutsaUser(AbstractBaseUser):
    nickname = models.CharField(max_length=64, unique=True) # 카카오 닉네임
    user_name = models.CharField(max_length=64, blank=True) #사용자로부터 받는 닉네임
    profile = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    refresh_token = models.CharField(max_length=256, blank=True)
    email = models.EmailField(max_length=64, blank=True) # 이메일
    school = models.CharField(max_length=64, blank=True) # 학교
    college = models.CharField(max_length=64, blank=True) # 단과대학


    objects = MutsaUserManager()

    USERNAME_FIELD = 'nickname'

    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta:
        db_table = 'mutsa_user'
 