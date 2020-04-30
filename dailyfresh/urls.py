"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^tinymce/', include('tinymce.urls')),  # 富文本编辑器
    # url(r'^search', include('haystack.urls')),  # 全文检索框架
    # url(r'^user/', include(('user.urls', 'user'), namespace='user')),  # 用户模块
    # url(r'^cart/', include(('cart.urls', 'cart'), namespace='cart')),  # 购物车模块
    # url(r'^order/', include(('order.urls', 'order'), namespace='order')),  # 订单模块
    # url(r'^', include(('goods.urls', 'goods'), namespace='goods')),  # 商品模块
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),  # 富文本编辑器
    path('search', include('haystack.urls')),  # 全文检索框架
    path('user/', include(('user.urls', 'user'), namespace='user')),  # 用户模块
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),  # 购物车模块
    path('order/', include(('order.urls', 'order'), namespace='order')),  # 订单模块
    path('', include(('goods.urls', 'goods'), namespace='goods')),  # 商品模块
]
