# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
import os

# 接收POST请求数据
def search_post(request):
    ctx = {}
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        emailinfo = request.FILES.get("emailinfo", None)
        emailmessage = request.FILES.get("emailmessage", None)

        emailLines = emailinfo.readlines()
        splitinfo = ":"

        from_addr = format_email(emailLines[1],splitinfo)
        password = format_email(emailLines[2],splitinfo)
        smtp_server = format_email(emailLines[3],splitinfo)
        emailtitle = format_email(emailLines[4],splitinfo)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        tenpufilepath = BASE_DIR+format_email(emailLines[5], splitinfo)
        tenpufilename = os.path.split(tenpufilepath)[1]

        # from_addr = 'liu@popunavi-soft.com'
        # password = 'xiaopihai771111'
        # smtp_server = 'smtp.muumuu-mail.com'

        # to_addr = 'popunavi@yahoo.co.jp'
        # emailaddress = open('/Users/liu/emaillist.txt', 'r')

        fileinfo = ""




        # 邮件正文是MIMEText:root@localhost: )rjf6Y<(y!7<
        # msg.attach(MIMEText(emailmessage.read().decode('utf-8').replace('●','ddddddd株式会社').replace('◎','ddddddd株式会社'), 'plain', 'utf-8'))

        emessage = emailmessage.read()
        i = 0
        companyname = ''
        # with open('/Users/liu/emaillist.txt', 'r') as emailaddress:
        #     for line in emailaddress.readlines():
        for line in myFile.readlines():
            msg = MIMEMultipart()
            msg['From'] = _format_addr(format_email(emailLines[0], splitinfo) + ' <%s>' % from_addr)

            msg['Subject'] = Header(emailtitle, 'utf-8').encode()

            fileinfo = line.decode('utf-8').split(splitinfo)[0].strip()
            companyname = line.decode('utf-8').split(splitinfo)[1].strip()
            personname = line.decode('utf-8').split(splitinfo)[2].strip()
            # companyname = companyname + companyname
            # 邮件正文是MIMEText:root@localhost: )rjf6Y<(y!7<
            msg.attach(
            MIMEText(emessage.decode('utf-8').replace('●', companyname)
                     .replace('◎', personname),'plain', 'utf-8'))

            # if i == 0:
            # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
            with open(tenpufilepath.encode('utf_8'), 'rb') as f:
                # 设置附件的MIME和文件名，这里是png类型:
                mime = MIMEBase('excel', tenpufilename.split(".")[1], filename=tenpufilename)
                # 加上必要的头信息:
                mime.add_header('Content-Disposition', 'attachment', filename=tenpufilename)
                mime.add_header('Content-ID', '<0>')
                mime.add_header('X-Attachment-Id', '0')
                # 把附件的内容读进来:
                mime.set_payload(f.read())
                # 用Base64编码:
                encoders.encode_base64(mime)
                # 添加到MIMEMultipart:
                msg.attach(mime)

            server = smtplib.SMTP(smtp_server, 25)
            server.set_debuglevel(1)
            server.login(from_addr, password)


            msg['To'] = _format_addr(' <%s>' % fileinfo.strip())
            server.sendmail(from_addr, [fileinfo.strip()], msg.as_string())
            i = i+1
        server.quit()


    # if request.POST:
        ctx['rlt'] = companyname

    return render(request, "post.html", ctx)


def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))


def format_email(a,b):
    return a.decode('utf-8').split(b)[1].strip()