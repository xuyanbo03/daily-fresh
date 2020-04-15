from django.urls import path
from . import views

app_name = 'goods'
urlpatterns = [
    path('', views.index, name='index')  # 首页
]
