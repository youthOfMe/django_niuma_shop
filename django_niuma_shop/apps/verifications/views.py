from django.http import HttpResponse, JsonResponse
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

# 配置短信验证码接口类
class SmsCodeView(View):

    def get(self, request, mobile):
        # 1. 获取请求参数
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 2. 验证参数
        if not all([image_code, uuid]):
            return JsonResponse({ 'code': 400, 'errmsg': '参数不全' })
        # 3. 验证图片验证码
        # 3.1 进行连接redis
        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('code')
        # 3.2 获取redis数据
        redis_image_code = redis_cli.get(uuid)
        # 3.3 进行对比图形验证码
        if not redis_image_code:
            return JsonResponse({ 'code': 400, 'errmsg': '图片验证码已过期或者不存在' })
        if image_code.lower() != redis_image_code.decode().lower():
            return JsonResponse({ 'code': 400, 'errimg': '图片验证码错误' })

        # 提取发送短信的标记 看看有没有
        send_flag = redis_cli.get('send_flag_%s'%mobile)

        if send_flag:
            return JsonResponse({ 'code': 400, 'errmsg': '不要频繁发送短信' })

        # 4. 生成短信验证码
        from random import randint
        sms_code = '%04d'%randint(0, 9999)

        # 5. 使用管道进行提交短信验证码和发送标记
        # 5.1. 新建一个管道
        pipeline = redis_cli.pipeline()
        # 5.2. 管道收集指令
        # 5.2.1. 进行保存短信验证码
        pipeline.setex(mobile, 300, sms_code)
        # 5.2.2 添加一个发送标记 有效期60秒
        pipeline.setex('send_flag_%s'%mobile, 60, 1)
        # 5.3 管道执行指令
        pipeline.execute()

        # 6. 采用celery进行异步发送短信
        from celery_tasks.sms.tasks import  celery_send_sms_code
        celery_send_sms_code.delay(mobile, sms_code)

        # 7. 返回响应
        return JsonResponse({ 'code': 0, 'errmsg': 'ok' })