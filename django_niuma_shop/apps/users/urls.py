from django.urls import path

from apps.users.views import UsernameCountView, UserModelCountView, RegisterView, LoginView

urlpatterns = [
    # 判断用户是否存在
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    path('mobiles/<str:mobile>/count/', UserModelCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view())
]