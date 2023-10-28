from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# 配置图片接口类
class ImageCodeView(View):

    def get(self, requesy, uuid):
        # 2. 生成图片验证码和图片二进制
        from libs.captcha.captcha import captcha
        # 返回验证码内容和二进制数据
        text, image = captcha.generate_captcha()
        # 3. 使用redis进行保存图片验证码保存起来
        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('code')
        redis_cli.setex(uuid, 100, text)
        # 4. 返回图片二进制数据
        return HttpResponse(image, content_type='image/jpeg')
