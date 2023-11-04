from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    identifier = models.CharField(max_length = 40, unique = True, default='')
    USERNAME_FIELD = 'identifier'
    mobile = models.CharField(max_length = 11, unique = True)
    email_active = models.BooleanField(default = False, verbose_name='邮箱验证状态')
    default_address = models.ForeignKey('Address', related_name='users', null = True, blank = True,
                                        on_delete=models.SET_NULL, verbose_name='默认地址mi')

    # 进行修改表名
    class Meta:
        # 在元信息类中重写表名
        db_table = "tb_users"
        # 定义数据库中admin后台显示的表的名称
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name

from utils.models import BaseModel

class Address(BaseModel):
    """用户地址"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses', verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses', verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']