import re
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django_redis import get_redis_connection
from user.models import *
from goods.models import *
from order.models import *
from celery_tasks.tasks import send_register_active_email
from utils.mixin import LoginRequiredMixin


# Create your views here.
# /user/register
def register(request):
    """注册"""
    if request.method == 'GET':
        # 显示注册页面
        return render(request, 'register.html')
    else:
        # 进行注册处理
        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        # 是否同意协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except:
            # 用户名不存在
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 进行业务处理：进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 发送激活邮件，包含激活链接：http://127.0.0.1:8000/user/active/id
        # 激活链接中需要包含用户的身份信息，并且要把身份信息进行加密

        # 加密用户的身份信息，生成激活的token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)
        token = token.decode()

        # 同步阻塞发邮件
        subject = '天天生鲜激活信息'
        message = ''
        sender = settings.EMAIL_FROM
        receiver = [email]
        html_message = '<h1>%s，欢迎您成为天天生鲜会员</h1><br />请点击下面链接激活您的账户：<br /><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
            username, token, token)
        send_mail(subject, message, sender, receiver, html_message=html_message)

        # 返回应答，跳转到首页
        return redirect(reverse('goods:index'))


# /user/register_handle
# def register_handle(request):
#     """进行注册处理"""
#     # 接受数据
#     username = request.POST.get('user_name')
#     password = request.POST.get('pwd')
#     email = request.POST.get('email')
#     allow = request.POST.get('allow')
#
#     # 进行数据校验
#     if not all([username, password, email]):
#         return render(request, 'register.html', {'errmsg': '数据不完整'})
#
#     # 校验邮箱
#     if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
#         return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
#
#     # 是否同意协议
#     if allow != 'on':
#         return render(request, 'register.html', {'errmsg': '请同意协议'})
#
#     # 校验用户名是否重复
#     try:
#         user = User.objects.get(username=username)
#     except:
#         # 用户名不存在
#         user = None
#
#     if user:
#         # 用户名已存在
#         return render(request, 'register.html', {'errmsg': '用户名已存在'})
#
#     # 进行业务处理：进行用户注册
#     user = User.objects.create_user(username, email, password)
#     user.is_active = 0
#     user.save()
#
#     # 返回应答，跳转到首页
#     return redirect(reverse('goods:index'))


# 使用类视图重构
# /user/register
class RegisterView(View):
    """注册"""

    def get(self, request):
        """显示注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """进行注册处理"""
        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        # 是否同意协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except:
            # 用户名不存在
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 进行业务处理：进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 发送激活邮件，包含激活链接：http://127.0.0.1:8000/user/active/id
        # 激活链接中需要包含用户的身份信息，并且要把身份信息进行加密

        # 加密用户的身份信息，生成激活的token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)
        token = token.decode()

        # 异步发邮件
        send_register_active_email.delay(email, username, token)

        # 返回应答，跳转到首页
        return redirect(reverse('goods:index'))


# /user/active
class ActiveView(View):
    """用户激活"""

    def get(self, request, token):
        """进行激活"""
        # 进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户id
            user_id = info['confirm']
            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转到登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('激活链接已过期')


# /user/login
class LoginView(View):
    """登录"""

    def get(self, request):
        """显示登录页面"""
        # 判断是否记住用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        """登录校验"""
        # 接受数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 进行数据校验
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        # 校验登录，返回应答，跳转到首页
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户密码正确
            if user.is_active:
                # 记录用户的登录状态
                login(request, user)
                # 获取登录后所要跳转的地址，默认跳转到首页
                next_url = request.GET.get('next', reverse('goods:index'))
                response = redirect(next_url)

                # 判断是否记住用户名
                remember = request.POST.get('remember')
                if remember == 'on':
                    # 记住用户名一周
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')

                # 返回应答
                return response
            else:
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            # 用户密码不正确
            return render(request, 'login.html', {'errmsg': '用户名或密码不正确'})


# /user/logout
class LogoutView(View):
    """退出登录"""

    def get(self, request):
        # 退出，并清除用户session
        logout(request)
        return redirect(reverse('goods:index'))


# /user
class UserInfoView(LoginRequiredMixin, View):
    """用户信息-信息页"""

    def get(self, request):
        """显示"""
        # 获取用户个人信息
        # 获取登录用户对应User对象
        user = request.user
        address = Address.objects.get_default_address(user)

        # 获取用户历史浏览记录
        # 历史浏览记录存储在redis中，连接redis
        con = get_redis_connection('default')
        history_key = 'history_%d' % user.id

        # 获取用户最新浏览的5个商品id
        sku_ids = con.lrange(history_key, 0, 4)
        # 从数据库中查询用户浏览商品具体信息，遍历获取
        # goods_li = GoodsSKU.objects.filter(id__in=sku_ids)  # 顺序不一致，故不采用
        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)

        # 组织上下文
        context = {'page': 'user', 'address': address, 'goods_li': goods_li}

        # 除了你给模板文件传递的变量之外，django框架会把request.user.is_authenticated()也传给模板文件
        return render(request, 'user_center_info.html', context)


# /user/order
class UserOrderView(LoginRequiredMixin, View):
    """用户信息-订单页"""

    def get(self, request, page):
        """显示"""
        # 获取用户订单信息
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')

        # 遍历获取订单商品信息
        for order in orders:
            # 根据order_id查询订单商品信息
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)

            # 遍历计算商品小计
            for order_sku in order_skus:
                # 计算小计
                amount = order_sku.count * order_sku.price
                # 动态给order_sku增加amount属性，保存订单商品小计
                order_sku.amount = amount

            # 动态给order增加属性，保存订单商品信息
            order.order_skus = order_skus
            order.status_name = OrderInfo.ORDER_STATUS[order.order_status]

        # 分页
        paginator = Paginator(orders, 1)

        # 处理页码
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        order_page = paginator.page(page)

        # 进行页码控制，页面上最多显示5个页码
        # 1. 总页数小于5页，页面上显示所有页码
        # 2. 如果当前页是前3页，显示1-5页
        # 3. 如果当前页是后3页，显示后5页
        # 4. 其他情况，显示当前页的前2页，当前页，当前页的后2页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        # 上下文
        context = {
            'order_page': order_page,
            'pages': pages,
            'page': 'order'
        }

        return render(request, 'user_center_order.html', context)


# /user/address
class AddressView(LoginRequiredMixin, View):
    """用户信息-地址页"""

    def get(self, request):
        """显示"""
        # 获取登录用户对应User对象
        user = request.user

        # 获取用户默认收货地址
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist as e:
        #     # 不存在默认收货地址
        #     address = None
        address = Address.objects.get_default_address(user)

        return render(request, 'user_center_site.html', {'page': 'address', 'address': address})

    def post(self, request):
        """地址添加"""
        # 接受数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 数据校验
        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html', {'errmsg': '数据不完整'})

        # 校验手机号
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机格式不正确'})

        # 业务处理：地址添加
        # 获取登录用户对应User对象
        user = request.user

        # 如果用户已存在默认收货地址，添加的地址不作为默认收货地址，否则作为默认
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist as e:
        #     # 不存在默认收货地址
        #     address = None
        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)

        # 返回应答，刷新地址页面，get请求
        return redirect(reverse('user:address'))
