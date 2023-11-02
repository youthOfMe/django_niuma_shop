from django.urls import path
from .views import AreaView

urlpatterns = [
    path('areas/', AreaView.as_view())
]