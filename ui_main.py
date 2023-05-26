from Login_Pane import LoginPane
from Register_Pane import RegisterPane
from PyQt5.Qt import *
# import pymysql
import yonghu_ui_main
import sqlite3
import os
# 控制各界面展现的是项目中的 Register_Pane.py(注册界面)、Login_Pane.py（登陆界面）
# 它们负责将每个界面前端布局有组件间的逻辑关系进行关联生成类，通过在 ui_main.py 中建立实例具体展现
# 首先是项目结构，在项目中，有个控制所有界面的 ui_main.py,
# 它负责控制整个项目的运行流程与界面切换，比如最开始运行项目要展示登陆界面，当点击“注册账号”时就要控制注册界面取代登陆界面。

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = QWidget()

    # 控件面板的创建
    login_pane = LoginPane()
    register_pane = RegisterPane(login_pane)
    register_pane.move(0, login_pane.height())
    login_pane.show()

    # 槽函数
    def exit_register_pane():
        animation = QPropertyAnimation(register_pane)#设置对象类
        animation.setTargetObject(register_pane)#设置仿真对象
        animation.setPropertyName(b"pos")
        animation.setStartValue(QPoint(0, 0))
        animation.setEndValue(QPoint(login_pane.width(), 0))#缩小
        animation.setDuration(500)
        animation.setEasingCurve(QEasingCurve.OutBounce)
        animation.start(QAbstractAnimation.DeleteWhenStopped)

    # def tiaozhuan():
    #     test2.Ui_MainWindow.show()

    def show_register_pane():
        animation = QPropertyAnimation(register_pane)#设置对象类
        animation.setTargetObject(register_pane)
        animation.setPropertyName(b"pos")
        animation.setStartValue(QPoint(0, login_pane.height()))
        animation.setEndValue(QPoint(0,0))
        animation.setDuration(500)
        animation.setEasingCurve(QEasingCurve.OutBounce)
        animation.start(QAbstractAnimation.DeleteWhenStopped)

    def check_login(account,pwd):
        # os.system('python main.py')
        try:
            # 检查用户名和密码是否匹配
            # conn = pymysql.connect(host='localhost', port=3306, user='root', password='nuliba520.', db='test')
            conn = sqlite3.connect('yonghu1.db')
            cursor = conn.cursor()
            # cursor.execute('SELECT COUNT(*) FROM users WHERE username=%s AND password=%s', (account, pwd))
            cursor.execute("SELECT COUNT(*) FROM users WHERE username=? ", (account,))
            result = cursor.fetchone()
            if result[0] > 0:
                cursor.execute("SELECT COUNT(*) FROM users WHERE username=? AND password=?", (account, pwd,))
                result1=cursor.fetchone()
                if result1[0]>0:
                    str1=account+"-"+pwd
                    with open('结果存放', 'a') as file_handle:  # .txt可以不自己新建,代码会自动新建
                        file_handle.write(str1)
                    QMessageBox.information(w, '登录成功', '登录成功')
                    login_pane.close()
                    register_pane.close()
                    os.system('python yonghu_ui_main.py')
                    # login_pane.zhuye_signal.emit()
                else:
                    QMessageBox.information(w, '错误', '密码错误')
            else:
                QMessageBox.information(w, '错误', '无此账号，请先注册')
            cursor.close()
        except sqlite3.Error as e:
            print(f'MySQL Error: {e}')

    # 信号的连接
    register_pane.exit_signal.connect(exit_register_pane)
    login_pane.check_login_signal.connect(lambda account,pwd:print(account,pwd))#用于槽信号接受值
    login_pane.show_register_pane_signal.connect(show_register_pane)
    login_pane.check_login_signal.connect(check_login)
    # tiaozhuan_signal.connect(tiaozhuan)
    # login_pane.zhuye_signal.connect(tiaozhuan)
    sys.exit(app.exec_())
