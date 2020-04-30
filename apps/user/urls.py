# from django.conf.urls import url
from django.urls import path, re_path
from .views import *

app_name = 'user'
urlpatterns = [
    # url(r'^register$', views.register, name='register')
    # path('register', views.register, name='register'),  # 注册
    # path('register_handle', views.register_handle, name='register_handle')  # 注册处理
    path('register', RegisterView.as_view(), name='register'),  # 注册

    # re_path(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 用户激活
    path('active/<str:token>', ActiveView.as_view(), name='active'),  # 用户激活

    path('login', LoginView.as_view(), name='login'),  # 登录
    path('logout', LogoutView.as_view(), name='logout'),  # 注销

    # path('', login_required(UserInfoView.as_view()), name='user'),  # 用户信息-信息页
    # path('order', login_required(UserOrderView.as_view()), name='order'),  # 用户信息-订单页
    # path('address', login_required(AddressView.as_view()), name='address'),  # 用户信息-地址页
    # 加入mixin，修改
    path('', UserInfoView.as_view(), name='user'),  # 用户信息-信息页
    # re_path(r'^order/(?P<page>\d+)$', UserOrderView.as_view(), name='order'),  # 用户信息-订单页
    path('order/<int:page>', UserOrderView.as_view(), name='order'),  # 用户信息-订单页
    path('address', AddressView.as_view(), name='address'),  # 用户信息-地址页
]
