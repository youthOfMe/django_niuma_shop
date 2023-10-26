import re

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.users.models import User


# 进行配置一个判断用户是否注册的接口
class UsernameCountView(View):
    def get(self, request, username):
        # 将前端传过来的数据进行查询数据库
        count = User.objects.filter(username = username).count()
        # 进行返回响应
        return JsonResponse({ 'code': 0, 'count': count, 'errmsg': 'ok' })

# 进行配置一个判断手机号是否已经注册的接口
class UserModelCountView(View):
    def get(self, request, mobile):
        # 1. 接收手机号对手机号进行正则判断
        if not re.match('^1[3-9]\d{9}$', mobile):
            return JsonResponse({ 'code': 400, 'errmsg': '手机号不符合格式' })
        # 2. 根据手机号进行查询数据库
        count = User.objects.filter(mobile = mobile).count()
        # 3. 返回响应
        return JsonResponse({ 'code': 0, 'count': count, 'errmsg': 'ok' })