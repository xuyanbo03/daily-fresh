#!/usr/bin/python3
# -*- coding:utf-8 -*-
from django.core.mail import send_mail
from django.conf import settings
from celery import Celery
import os
import django

# 任务处理者一端添加
# 终端命令：celery -A celery_tasks.tasks worker --pool=solo -l info
# 设置环境变量
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
# 设置django初始化
#django.setup()

# 创建一个Celery类的实例对象
app = Celery('celery_tasks.tasks', broker='redis://192.168.123.130:6379/8')


# 定义任务函数
@app.task
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""
    subject = '天天生鲜激活信息'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s，欢迎您成为天天生鲜会员</h1><br />请点击下面链接激活您的账户：<br /><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
        username, token, token)
    send_mail(subject, message, sender, receiver, html_message=html_message)
