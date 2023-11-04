from django.urls import path

from apps.users.views import UsernameCountView, UserModelCountView, RegisterView, LoginView, LogoutView, CenterView, EmailView
from apps.users.views import AddressCreateView, AddressView

urlpatterns = [
    # 判断用户是否存在
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    path('mobiles/<str:mobile>/count/', UserModelCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('info/', CenterView.as_view()),
    path('emails/', EmailView.as_view()),
    path('addresses/create/', AddressCreateView.as_view()),
    path('addresses/', AddressView.as_view()),
]