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

