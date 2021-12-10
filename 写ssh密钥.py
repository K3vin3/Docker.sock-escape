#! /usr/bin/python
# -*- coding: utf-8 -*-

import docker
import socks
import socket
import sys
import re

#开启代理
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1081)
#socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 1081)
socket.socket = socks.socksocket

ip = '172.16.145.165'
cli = docker.DockerClient(base_url='tcp://'+ip+':2375', version='auto') 
#端口不一定为2375，指定version参数是因为本机和远程主机的API版本可能不同，指定为auto可以自己判断版本
image = cli.images.list()[0]

#读取生成的公钥
f = open('id_rsa_2048.pub', 'r')
sshKey = f.read()
f.close()

try:
    cli.containers.run(
        image=image.tags[0], 
        command='sh -c "echo '+sshKey+' >> /usr/games/authorized_keys"', #这里卡了很久，这是正确有效的写法，在有重定向时直接写命令是无法正确执行的，记得加上sh -c
        volumes={'/root/.ssh':{'bind': '/usr/games', 'mode': 'rw'}}, #找一个基本所有环境都有的目录
        name='test' #给容器命名，便于后面删除
    )
except docker.errors.ContainerError as e:
    print(e)

#删除容器
try:
    container = cli.containers.get('test')
    container.remove()
except Expection as e:
    continue
