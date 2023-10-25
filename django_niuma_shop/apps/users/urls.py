from django.urls import path

from apps.users.views import UsernameCountView

urlpatterns = [
    # 判断用户是否存在
    path('usernames/<username:username>/count/', UsernameCountView.as_view())
]