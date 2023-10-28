from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
# 引入转换器的包
from utils.converters import UsernameConverter
from django.urls import register_converter

def log(request):

    # 1.进行导入日志模块
    import logging
    # 2.创建日志器
    logger = logging.getLogger('django')
    # 3. 调用日志器的方法来保存日志
    logger.info('用户登录了')
    logger.warning("redis缓存不足")
    logger.error("该记录不存在")
    logger.debug("正在进行调式")
    return HttpResponse('log')

# 进行注册校验用户名的正则表达式
register_converter(UsernameConverter, 'username')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('log/', log),
    # 配置apps.users子应用中的路由函数
    path('', include('apps.users.urls')),
    # 配置apps.verification子应用中的路由函数
    path('', include('apps.verifications.urls')),
]
