from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.utils.translation import gettext_lazy as _


class UserType(models.Model):
    user_type = models.CharField(max_length=50)  # candidate, recruiter

    class Meta:
        db_table = "user_types"

    def __str__(self):
        return self.user_type


# custom user model 사용 시 UserManager 클래스와 create_user, create_superuser 함수가 정의되어 있어야 함
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an username")
        user = self.model(
            # username=username,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, email, password=None):
        user = self.create_user(
            # username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    # username = models.CharField("사용자 계정", max_length=20, unique=True)
    # email = models.EmailField("이메일 주소", max_length=100)
    # password = models.CharField("비밀번호", max_length=128)
    # fullname = models.CharField("이름", max_length=20)
    # join_date = models.DateTimeField("가입일", auto_now_add=True)
    user_type = models.ForeignKey(
        "UserType", on_delete=models.SET_NULL, null=True
    )  # user_type + _id
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    fullname = models.CharField(max_length=20)
    join_date = models.DateTimeField(auto_now_add=True)

    # is_active가 False일 경우 계정이 비활성화됨
    is_active = models.BooleanField(default=True)

    # is_staff에서 해당 값 사용
    is_admin = models.BooleanField(default=False)

    # id로 사용 할 필드 지정.
    # 로그인 시 USERNAME_FIELD에 설정 된 필드와 password가 사용된다.
    USERNAME_FIELD = "email"

    # user를 생성할 때 입력받은 필드 지정
    REQUIRED_FIELDS = []

    objects = UserManager()  # custom user 생성 시 필요

    def __str__(self):
        # return self.username
        return self.email

    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_perm(self, perm, obj=None):
        return True

    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_module_perms(self, app_label):
        return True

    # admin 권한 설정
    @property
    def is_staff(self):
        return self.is_admin


class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_login_date = models.DateField()
    last_job_apply_date = models.DateField(null=True)

    class Meta:
        db_table = "user_logs"
