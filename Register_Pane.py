from PyQt5.Qt import *
from resource.register import Ui_Form
import pymysql
import sqlite3
import re
# import yz
class RegisterPane(QWidget, Ui_Form):
    exit_signal = pyqtSignal()
    register_account_pwd_signal = pyqtSignal(str,str)

    def __init__(self, parent=None, *args, **kwargs):#可以传入接受任意个数的参数
        super().__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)#是顶级页面背景生效
        self.setupUi(self)
        # self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='nuliba520.', db='test')
        self.conn = sqlite3.connect('yonghu1.db')
        self.animation_targets=[self.about_menu_btn,self.reset_menu_btn,self.exit_menu_btn]
        self.animation_targets_pos = [target.pos() for target in self.animation_targets]#把按钮的位置加入animation_targets_pos

    def show_hide_menu(self,checked):
        print("显示和隐藏",checked)

        animation_group = QSequentialAnimationGroup(self)#串行动画小组，即把动画导入其中按顺序执行
        for idx,target in enumerate(self.animation_targets):#idx为标签与坐姿识别一致
            animation = QPropertyAnimation()#对象类
            animation.setTargetObject(target)#设置仿真对象
            animation.setPropertyName(b"pos")#设置仿真属性的名称
            animation.setStartValue(self.main_menu_btn.pos())#设置初始值，即主菜单位置
            animation.setEndValue(self.animation_targets_pos[idx])#把按钮放回到原始地方
            animation.setDuration(100)#设置持续时间为0.1s
            animation.setEasingCurve(QEasingCurve.OutBounce)#动画变化中的缓和曲线
            animation_group.addAnimation(animation)#小组把动画添加
        if not checked:
            animation_group.setDirection(QAbstractAnimation.Forward)
        else:
            animation_group.setDirection(QAbstractAnimation.Backward)
        animation_group.start(QAbstractAnimation.DeleteWhenStopped)#对象运行完，停止后自动删除

    def show_about_menu(self):
        print("关于")
        QMessageBox.about(self, "方法使用","该软件可以实现坐姿检测，使您保持一个好的坐姿"
                                       "<br>1:当持续3s坐姿不端正会语音提醒。"
                                       "<br>2:请填写qq邮箱 持续30s坐姿不端正将会发送邮件提醒")

    def show_reset_menu(self):
        print("重置")
        self.account_le.clear()
        self.password_le.clear()
        self.confirm_pwd_le.clear()
        self.account_le_2.clear()
        self.account_le_3.clear()

    def show_exit_menu(self):
        self.exit_signal.emit()

    def register(self):
        account_txt = self.account_le.text()
        password_txt = self.password_le.text()
        number_txt=self.account_le_2.text()
        qq_number_txt=self.account_le_3.text()
        # if yz.duanxin_yz():
        #     yzm=yz.duanxin_yz()
        # print(yzm)
        # num, ok = QInputDialog.getText(self, '手机号验证', '输入验证码')
        # if num!=yzm:
        #     QMessageBox.information(self, '坐姿识别', '验证码错误，请一分钟之后再次发送')
        # else:
        try:
            # 创建用户
            cursor = self.conn.cursor()
            # sql_text_1 = '''CREATE TABLE users
            #            (username VARCHAR(45) PRIMARY KEY NOT NULL ,
            #             password VARCHAR(45) NOT NULL  ,
            #             phonenumber VARCHAR(45) NOT NULL UNIQUE ,
            #             email VARCHAR(45) NOT NULL UNIQUE );'''
            # cursor.execute(sql_text_1)
            # sql_text_2 = "INSERT INTO users (username, password,phonenumber,email) VALUES (%s, %s,%s,%s)', (account_txt, password_txt,number_txt,qq_number_txt)"
            # cursor.execute('INSERT INTO users (username, password,phonenumber,email) VALUES (%s, %s,%s,%s)', (account_txt, password_txt,number_txt,qq_number_txt))
            cursor.execute("INSERT INTO users (username, password,phonenumber,email) VALUES (?, ?,?,?)", (account_txt, password_txt,number_txt,qq_number_txt))
            self.conn.commit()
            QMessageBox.information(self, '注册', '注册成功')
            self.account_le.clear()
            self.password_le.clear()
            self.confirm_pwd_le.clear()
            self.account_le_2.clear()
            self.account_le_3.clear()
            cursor.close()
        except sqlite3.Error as e:
            if str(e)=="UNIQUE constraint failed: users.username":
                QMessageBox.information(self, '错误', '账号已被注册')
            if str(e)=="UNIQUE constraint failed: users.phonenumber":
                QMessageBox.information(self, '错误', '电话号码已被注册')
            if str(e)=="UNIQUE constraint failed: users.email":
                QMessageBox.information(self, '错误', '已被注册')
            print(f'MySQL Error: {e}')

    def enable_register_btn(self):
        account_txt = self.account_le.text()
        password_txt = self.password_le.text()
        cp_txt = self.confirm_pwd_le.text()
        number_txt=self.account_le_2.text()
        qq_number_txt=self.account_le_3.text()
        ret = re.match(r"^1[35678]\d{9}$", number_txt)
        if len(account_txt)>0 and len(password_txt)>0 and len(cp_txt)>0 and password_txt==cp_txt and ret!=None and len(qq_number_txt)>0:
            self.register_btn.setEnabled(True)
        else:
            self.register_btn.setEnabled(False)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = RegisterPane()
    window.exit_signal.connect(lambda :print("退出"))
    # window.register_account_pwd_signal.connect(lambda sig1,sig2:print(sig1,sig2))
    window.show()
    sys.exit(app.exec_())
