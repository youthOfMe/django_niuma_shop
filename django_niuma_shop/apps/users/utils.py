from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django_niuma_shop import settings

def generic_email_verify_token(user_id):

    # 1. 创建实例
    s = Serializer(secret_key=settings.SECRET_KEY, expires_in = 3600*24)
    # 2. 加密数据
    data = s.dump({ 'user_id': user_id })
    # 3. 返回数据
    return data.decode()
