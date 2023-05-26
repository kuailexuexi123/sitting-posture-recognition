import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# my_sender = '463626021@qq.com'  # 填写发信人的邮箱账号
# my_pass = 'ildfydfcmeoybheb'  # 发件人邮箱授权码
# my_user = '835352240@qq.com'  # 收件人邮箱账号


def mail(my_user1):
    my_sender = '463626021@qq.com'  # 填写发信人的邮箱账号
    my_pass = 'touhmgspfepubjjd'  # 发件人邮箱授权码
    my_user = my_user1+'@qq.com'  # 收件人邮箱账号
    ret = True
    try:
        msg = MIMEText('您的坐姿不端正，请及时调整', 'plain', 'utf-8')  # 填写邮件内容
        msg['From'] = formataddr(["坐姿识别系统", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["用户", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "坐姿识别提醒"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


# ret = mail()
# if ret:
#     print("邮件发送成功")
# else:
#     print("邮件发送失败")
