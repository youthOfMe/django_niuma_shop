import re

from django.contrib.auth.hashers import check_password
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

# 进行配置一个注册功能的接口类
import json
class RegisterView(View):

    def post(self, request):
        # 1. 获取数据
        # 获取前端发过来的json数据
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)

        # 2. 进行获取数据
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        allow = body_dict.get('allow')

        # 3. 进行校验数据
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({ 'code': 400, 'errmsg': "用户参数缺失" })

        # 验证用户是否存在以及符合规则
        user = User.objects.filter(username = username).first()
        if user:
            return JsonResponse({ 'code': 400, 'errmsg': '用户已存在' })
        if not re.match('[a-zA-Z_-]{5,20}', username):
            return JsonResponse({ 'code': 400, 'errmsg': '用户名不满足规则' })

        # 验证密码是否符合规则
        if len(password) > 20 or len(password) < 8:
            return JsonResponse({ 'code': 400, 'errmsg': '密码不满足规则' })

        # 验证确认密码和密码是否相同
        if password2 != password:
            return JsonResponse({ 'code': 400, 'errmsg': '两次密码输入不一致' })

        # 验证手机号格式是否正确
        if not re.match('^1[3-9]\d{9}$', mobile):
            return JsonResponse('手机号格式不正确')

        # 验证是否同意协议
        if not allow:
            return JsonResponse({ 'code': 400, 'errmsg': '请同意协议' })

        # 4. 数据入库
        # 使用django内置的方法进行加密密码字段数据
        import uuid
        user = User.objects.create_user(username = username, password = password, mobile = mobile, identifier = uuid.uuid4().hex)

        # 5.使用session配合redis实现状态持久化
        # 采用django内置的方法进行设置session
        from django.contrib.auth import login
        login(request, user)

        # 6. 进行返回响应
        return JsonResponse({ 'code': 0, 'errmsg': '用户注册成功' })

        # 7. 关闭crsf防御中间件

# 进行配置一个登录类
class LoginView(View):

    def post(self, request):
        # 1. 进行获取数据
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')

        # 2. 进行验证数据
        if not all([username, password]):
            return JsonResponse({ 'code': 400, 'errmsg': '参数不全' })

        # 3. 进行验证用户名和密码是否正确
        if not(re.match('1[3-9]\d{9}', username) or re.match('[a-zA-Z_-]{5,20}', username)):
            return JsonResponse({ 'code': 400, 'errmsg': '用户名或手机号格式错误' })

        user = User.objects.filter(username = username).first() or User.objects.filter(mobile = username).first()
        if not (user and check_password(password, user.password)):
            return JsonResponse({ 'code': 400, 'errmsg': '用户数据不存在或者密码错误' })
        # authenticate 用户名和密码对也返回false 很奇怪

        # 4. 设置session
        from django.contrib.auth import login
        login(request, user)

        # 5. 判断是否记住登录
        if remembered:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)

        # 6. 返回响应和设置session
        response = JsonResponse({ 'code':0, 'errmsg': 'ok' })
        # 进行设置cookie
        response.set_cookie('username', user.username)
        return response

# 实现退出登录的功能
from django.contrib.auth import logout
class LogoutView(View):

    def delete(self, request):
        # 1. 进行删除session信息
        logout(request)

        response = JsonResponse({ 'code': 0, 'errmsg': 'ok' })
        # 2. 删除cookie信息
        response.delete_cookie('username')

        return response

# 进行配置用户中心接口类
from utils.view import LoginRequiredJSONMixin
class CenterView(LoginRequiredJSONMixin, View):

    def get(self, request):

        info_data = {
            'username': request.user.username,
            'email': request.user.email,
            'mobile': request.user.mobile,
            'email_active': request.user.email_active,
        }

        return JsonResponse({ 'code': 0, 'errmsg': 'ok', 'info_data': info_data })

# 配置设置邮箱接口类
class EmailView(LoginRequiredJSONMixin, View):

    def put(self, request):
        # 1. 接收请求
        data = json.loads(request.body.decode())
        # 2. 获取数据
        email = data.get('email')
        # 3. 验证数据
        if not (all([email]) and re.match('^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email)):
            return JsonResponse({ 'code': 400, 'errmsg': '邮箱格式不正确' })

        # 4. 保存邮箱地址
        user = request.user
        user.email = email
        user.save()

        # 5. 进行发送一封激活邮件
        subject = '牛马商城激活验证消息'
        message = ''
        from_email = '牛马商城全球授权商<15315382573@163.com>'
        recipient_list = [email]
        from .utils import generic_email_verify_token
        token = generic_email_verify_token(request.user.id)
        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=%s'%token
        html_message = '<p>尊敬的老铁你好!</p>' \
                        '<p>感谢您访问牛马商城</p>' \
                        '<p>您的邮箱是: %s 请您点击此连接激活您的邮箱:</p>' \
                        '<p><a href="%s">%s</a></p>' % (email, verify_url, verify_url)
        from celery_tasks.email.tasks import celery_send_email
        celery_send_email.delay(
            subject = subject,
            message = message,
            from_email = from_email,
            recipient_list = recipient_list,
            html_message = html_message
        )

        #6. 返回响应
        return JsonResponse({ 'code': 0, 'errmsg': 'ok' })
