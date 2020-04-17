from django.urls import path
from .views import *

app_name = 'goods'
urlpatterns = [
    path('', IndexView.as_view(), name='index')  # 首页
]
