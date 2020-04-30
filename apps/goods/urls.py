from django.urls import path, re_path
from .views import *

app_name = 'goods'
urlpatterns = [
    path('index', IndexView.as_view(), name='index'),  # 首页
    # re_path(r'^goods/(?P<goods_id>\d+)$', DetailView.as_view(), name='detail'),  # 详情页
    path('goods/<int:goods_id>', DetailView.as_view(), name='detail'),  # 详情页
    # re_path(r'^list/(?P<type_id>\d+)/(?P<page>\d+)$', ListView.as_view(), name='list'),  # 列表页
    path('list/<int:type_id>/<int:page>', ListView.as_view(), name='list'),  # 列表页
]
