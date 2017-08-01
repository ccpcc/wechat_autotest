import itchat
import json
import datetime
import time
import os
from itchat.content import *

o=[]
b=[]
m=[21]
f=open("config.txt","r")
m[0]=int(f.read())
f.close()

def check_d(name):
    fo=open("during.json","r")
    c=fo.read()
    fo.close()
    c=json.loads(c)
    if name in c:
        return True
    else:
        return False

def del_d(name):
    fo=open("during.json","r")
    c=fo.read()
    fo.close()
    c=json.loads(c)
    c.remove(name)
    s=json.dumps(c)
    fo=open("during.json","w")
    fo.write(s)
    fo.close()

def write_d(name):
    fo=open("during.json","r")
    c=fo.read()
    fo.close()
    c=json.loads(c)
    c.append(name)
    s=json.dumps(c)
    fo=open("during.json","w")
    fo.write(s)
    fo.close()

    
def read_file(name):
    fo=open(name,"r")
    c=fo.readlines()
    for i in range(0,len(c)):
        c[i]=c[i].strip("\n")
    fo.close()
    return c

def write_file(name,content):
    if os.path.exists(name):
        fo=open(name,'a')
        fo.write(content)
        fo.close()
    else:
        fo=open(name,'w')
        fo.write(content)
        fo.close()
        
def check_time(s,l):
    s=datetime.datetime.strptime(s,'%Y-%m-%d-%H-%M-%S')
    l=datetime.datetime.strptime(l,'%Y-%m-%d-%H-%M-%S')
    c=(l-s).seconds
    h=c//3600
    m=(c-(h*3600))//60
    c=(c-(h*3600))-(m*60)
    return "用时%d小时%d分%d秒"%(h,m,c)

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    #itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])
    if not os.path.exists(itchat.search_friends(userName=msg["FromUserName"])["NickName"]):
        os.mkdir(itchat.search_friends(userName=msg["FromUserName"])["NickName"])
    if check_d(msg['FromUserName']):
        if msg['Text']=="交卷":
            del_d(msg['FromUserName'])
            o.append(msg['FromUserName'])
            t=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

            fn=itchat.search_friends(userName=msg["FromUserName"])["NickName"]+"/"+msg['FromUserName']+".txt"
            st=read_file(fn)[1]
            zt=check_time(st,t)
            c=t+"\n"
            write_file(fn,c)
            write_file(fn,zt+"\n")
            itchat.send('（来自Python脚本的自动回复）交卷成功！',msg['FromUserName'])
            itchat.send('（来自Python脚本的自动回复）%s'%zt,msg['FromUserName'])
        else:
            t=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
            fn=itchat.search_friends(userName=msg["FromUserName"])["NickName"]+"/"+msg['FromUserName']+".txt"
            st=read_file(fn)[1]
            zt=check_time(st,t)
            itchat.send('（来自Python脚本的自动回复）已%s'%zt,msg['FromUserName'])
            itchat.send('（来自Python脚本的自动回复）回复： 交卷  会停止计时，之后提交的答案无效',msg['FromUserName'])
    elif msg['FromUserName'] in o:
        itchat.send('（来自Python脚本的自动回复）已完成联考，请耐心等待判卷与答案公布',msg['FromUserName'])
        o.remove(msg['FromUserName'])
    elif msg['FromUserName'] in b:
        if msg['Text']=="helloworld":
            b.remove(msg['FromUserName'])
            itchat.send('（来自Python脚本的自动回复）已恢复自动回复',msg['FromUserName'])
    else:
        if msg['Text']=="发卷":
            write_d(msg['FromUserName'])
            t=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
            fn=itchat.search_friends(userName=msg["FromUserName"])["NickName"]+"/"+msg['FromUserName']+".txt"
            c=t+"\n"
            num="m1%d\n"%m[0]
            write_file(fn,num)#考号
            m[0]=m[0]+1
            f=open("config.txt","w")
            f.write(str(m[0]))
            f.close()
            
            write_file(fn,c)
            itchat.send('（来自Python脚本的自动回复）你的考号是%s'%num,msg['FromUserName'])
            itchat.send_file("questions.pdf",msg['FromUserName'])
            itchat.send_file("paper.pdf",msg['FromUserName'])
            itchat.send('（来自Python脚本的自动回复）成功获取试题！计时开始！',msg['FromUserName'])
            itchat.send('（来自Python脚本的自动回复）现在你可以通过文件、图片等形式提交答案，可以提交多个文件或多次提交',msg['FromUserName'])
            itchat.send('（来自Python脚本的自动回复）回复： 交卷  会停止计时，之后提交的答案无效',msg['FromUserName'])
        elif msg['Text']=="莫洛托夫":
            itchat.send('（来自Python脚本的自动回复）回复： 发卷  获得试卷并开始计时',msg['FromUserName'])
        elif msg['Text']=="886":
            b.append(msg['FromUserName'])
            itchat.send('（来自Python脚本的自动回复）已关闭，回复： helloworld  恢复自动回复',msg['FromUserName'])
        else:
            itchat.send('（来自Python脚本的自动回复）你好，有关莫洛托夫计划暑假联考请回复：莫洛托夫',msg['FromUserName'])
            itchat.send('（来自Python脚本的自动回复）不想接收自动回复请回复：886',msg['FromUserName'])

@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):
    if not os.path.exists(itchat.search_friends(userName=msg["FromUserName"])["NickName"]):
        os.mkdir(itchat.search_friends(userName=msg["FromUserName"])["NickName"])
    if check_d(msg["FromUserName"]):
        with open(itchat.search_friends(userName=msg["FromUserName"])["NickName"]+"/"+msg['FileName'], 'wb') as f:
            f.write(msg['Text']())
        itchat.send('（来自Python脚本的自动回复）已保存！',msg['FromUserName'])
    elif msg['FromUserName'] in o:
        itchat.send('（来自Python脚本的自动回复）交卷后无法再提交答案',msg['FromUserName'])
    elif msg['FromUserName'] in b:
        pass
    else:
        itchat.send('（来自Python脚本的自动回复）你好，有关莫洛托夫计划暑假联考请回复：莫洛托夫',msg['FromUserName'])
        itchat.send('（来自Python脚本的自动回复）不想接收自动回复请回复：886',msg['FromUserName'])
        
itchat.auto_login()
itchat.run()

