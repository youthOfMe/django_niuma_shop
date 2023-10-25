from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    identifier = models.CharField(max_length = 40, unique = True, default='')
    USERNAME_FIELD = 'identifier'
    mobile = models.CharField(max_length = 11, unique = True)

    # 进行修改表名
    class Meta:
        # 在元信息类中重写表名
        db_table = "tb_users"
        # 定义数据库中admin后台显示的表的名称
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name