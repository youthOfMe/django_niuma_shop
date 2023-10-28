# 0. 为celery的运行设置django的环境
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_niuma_shop.settings')

# 1. 创建celery实例
from celery import Celery
app = Celery('celery_tasks')

# 2. 设置broker 消息队列
# 进行加载broker
app.config_from_object('celery_tasks.config')

# 3. 使用celery进行自动检测包的任务 进行方便调用生产者生产任务
app.autodiscover_tasks(['celery_tasks.sms'])