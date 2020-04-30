from django.urls import path
from .views import *

app_name = 'order'

urlpatterns = [
    path('place', OrderPlaceView.as_view(), name='place'),  # 提交订单显示
    path('commit', OrderCommitView.as_view(), name='commit'),  # 订单创建
    path('pay', OrderPayView.as_view(), name='pay'),  # 订单支付
    path('check', CheckPayView.as_view(), name='check'),  # 订单支付验证
    path('comment/<int:order_id>', CommentView.as_view(), name='comment'),  # 订单支付验证
]
