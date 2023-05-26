import os
import sys
import winsound
import cv2
import mediapipe as mp
import time
import pyttsx3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PIL import Image, ImageDraw, ImageFont
from PyQt5_yemian.Head_detections import Head_detection
from PyQt5_yemian.Physical_detections import Physical_detection
from PyQt5_yemian.Squint_detections import Squint_detection
from PyQt5_yemian.Head_forwards import Head_forward
import sqlite3
import emails as em
# import pymysql
# my_sender = '463626021@qq.com'  # 填写发信人的邮箱账号
# my_pass = 'ildfydfcmeoybheb'  # 发件人邮箱授权码
# my_user = '835352240@qq.com'  # 收件人邮箱账号
# cuowu_time=0
class poseDetector():

    def __init__(self,mode= False,complex=1,smooth=True,enable=False,segment=True,
                 detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.complex=complex
        self.smooth=smooth
        self.enable=enable
        self.segment=segment
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        self.mpDraw=mp.solutions.drawing_utils
        self.mpPose=mp.solutions.pose #人体姿态检测
        self.pose=self.mpPose.Pose(self.mode,self.complex,self.smooth,self.enable,self.segment,
                                   self.detectionCon,self.trackCon)#姿态关键点检测函数
    def findpose(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 将导入的BGR格式图像转为RGB格式
        self.results = self.pose.process(imgRGB)  # 将图像传给姿态识别模型
        if self.results.pose_landmarks: # 如果采集到图像
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)  # 绘制姿态坐标点，img为画板，传入姿态点坐标，坐标连线
        return img
    def findPosition(self,img,draw=True):
        lmList=[]
        if self.results.pose_landmarks:
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x * w),int(lm.y * h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),5,(255,0,0),cv2.FILLED)
        return lmList

def jinggao():
    pt =pyttsx3.init()
    pt.say("请调整坐姿")
    pt.runAndWait()

class Voice_Thread(QThread):
    sinout = pyqtSignal(int)
    def __init__(self):
        super(Voice_Thread, self).__init__()

    def run(self):
        # 需要执行的内容
        jinggao()
        # print(yonghu_email)
        # print(em.mail(yonghu_email))
        # 发出信号
        self.sinout.emit(1)

class Email_Thread(QThread):
    sinout1=pyqtSignal(int)
    def __init__(self):
        super(Email_Thread, self).__init__()

    def run(self):
        # 需要执行的内容
        # jinggao()
        # print(yonghu_email)
        print(em.mail(yonghu_email))
        # 发出信号
        self.sinout1.emit(1)

class Ui_MainWindow(QtWidgets.QWidget):

    # zhuyemian_signal = pyqtSignal()
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.timer_camera = QtCore.QTimer()  # 初始化定时器
        self.cap = cv2.VideoCapture()  # 初始化摄像头
        self.CAM_NUM = 0
        self.set_ui()
        self.slot_init()
        self.__flag_work = 0
        self.x = 0
        self.count = 0
        self.voice_cuowu_time=0
        self.email_cuowu_time=0
        self.pose1=poseDetector()
        self.lmList=[]
        self.pTime = 0
        self.timeThread = Voice_Thread()
        self.timeThread.sinout.connect(self.show_Stop)
        self.timeThread1=Email_Thread()
        self.timeThread1.sinout1.connect(self.show_Stop1)

    def show_Stop(self):
        print("完成语音播报")

    def show_Stop1(self):
        print("完成短信发送")

    def set_ui(self):
        self.__layout_main = QtWidgets.QHBoxLayout()  # 采用QHBoxLayout类，按照从左到右的顺序来添加控件
        self.__layout_xinxi=QtWidgets.QVBoxLayout()
        self.__layout_fun_button = QtWidgets.QHBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()  # QVBoxLayout类垂直地摆放小部件

        self.button_open_camera = QtWidgets.QPushButton(u'开始识别')
        self.button_close = QtWidgets.QPushButton(u'退出')

        # button颜色修改
        button_color = [self.button_open_camera, self.button_close]
        for i in range(2):
            button_color[i].setStyleSheet("QPushButton{color:black}"
                                           "QPushButton:hover{color:red}"
                                           "QPushButton{background-color:rgb(78,255,255)}"
                                           "QpushButton{border:2px}"
                                           "QPushButton{border_radius:10px}"
                                           "QPushButton{padding:2px 4px}")

        self.button_open_camera.setMinimumHeight(50)
        self.button_close.setMinimumHeight(50)

        # move()方法是移动窗口在屏幕上的位置到x = 500，y = 500的位置上
        self.move(500, 300)

        # 信息显示
        self.label_show_camera = QtWidgets.QLabel()
        self.label_move = QtWidgets.QLabel()
        self.label_move.setFixedSize(100, 100)

        self.label_yonghuxinxi=QtWidgets.QLabel()
        str1="用户账号"+":"+str(yonghu_name)
        self.label_yonghuxinxi.setText(str1)

        self.label_show_camera.setFixedSize(641, 481)
        self.label_show_camera.setAutoFillBackground(False)

        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_close)
        self.__layout_fun_button.addWidget(self.label_move)

        self.__layout_xinxi.addWidget(self.label_yonghuxinxi)
        self.__layout_xinxi.addLayout(self.__layout_fun_button)
        self.__layout_main.addLayout(self.__layout_xinxi)
        self.__layout_main.addWidget(self.label_show_camera)

        self.setLayout(self.__layout_main)
        self.label_move.raise_()
        self.setWindowTitle(u'坐姿识别')

        '''
        # 设置背景颜色
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(),QBrush(QPixmap('background.jpg')))
        self.setPalette(palette1)
        '''

    def slot_init(self):  # 建立通信连接
        self.button_open_camera.clicked.connect(self.button_open_camera_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.button_close.clicked.connect(self.close)
        # self.zhuyemian_signal.connect(self.jinggao)

    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
                # if msg==QtGui.QMessageBox.Cancel:
                #                     pass
            else:
                self.timer_camera.start(50)
                self.button_open_camera.setText(u'关闭识别')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.button_open_camera.setText(u'开启识别')

    def show_camera(self):
        Head_detection_data = []
        Physical_detection_data = []
        Squint_detection_data = []
        Head_forward_data = []
        true_sit = 1
        head_left = 1
        head_right = 1
        body_left = 1
        body_right = 1
        squint = 1
        head_forward = 1
        flag, self.image = self.cap.read()
        cTime = time.time()
        fps = 1 / (cTime - self.pTime)
        self.pTime = cTime
        cv2.putText(self.image,str(int(fps)),(30,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        cv2.putText(self.image, "Head tilt left", (30, 125), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        cv2.putText(self.image, "Head tilt right", (30, 150), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        cv2.putText(self.image, "Body tilt to the lefe", (30, 175), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        cv2.putText(self.image, "Body tilt to the right", (30, 200), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        cv2.putText(self.image, "Squint", (30, 225), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        cv2.putText(self.image, "Head forwards", (30, 250), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        cv2.putText(self.image, "Sit correctly", (30, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        self.image=self.pose1.findpose(self.image)
        self.lmList=self.pose1.findPosition(self.image)
        # print(self.lmList)
        if len(self.lmList)>0:
            Head_detection_data.append(self.lmList[0][2])
            Physical_detection_data.append(self.lmList[0][2])
            Squint_detection_data.append(self.lmList[0][1])
            Head_forward_data.append(self.lmList[0][2])
            Head_detection_data.append(self.lmList[2][2])
            Head_detection_data.append(self.lmList[5][2])
            Physical_detection_data.append(self.lmList[11][2])
            Squint_detection_data.append(self.lmList[11][1])
            Head_forward_data.append(self.lmList[11][2])
            Physical_detection_data.append(self.lmList[12][2])
            Squint_detection_data.append(self.lmList[12][1])
            Head_forward_data.append(self.lmList[12][2])
            if Head_detection(Head_detection_data) == 1:
                cv2.putText(self.image, "Head tilt left", (30, 125), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                true_sit = 0
                head_left = 0
            if Head_detection(Head_detection_data) == 2:
                cv2.putText(self.image, "Head tilt right", (30, 150), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                true_sit = 0
                head_right = 0
            if Physical_detection(Physical_detection_data) == 2:
                cv2.putText(self.image, "Body tilt to the lefe", (30, 175), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                true_sit = 0
                body_left = 0
            if Physical_detection(Physical_detection_data) == 3:
                cv2.putText(self.image, "Body tilt to the right", (30, 200), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                true_sit = 0
                body_right = 0
            if Squint_detection(Squint_detection_data) == 2:
                cv2.putText(self.image, "Squint", (30, 225), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                true_sit = 0
                squint = 0
            if Head_forward(Head_forward_data) == 1:
                cv2.putText(self.image, "Head forwards", (30, 250), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                true_sit = 0
                head_forward = 0
            if head_left==0 or head_right==0 or body_left==0 or body_right==0 or squint==0 or head_forward==0 :
                self.voice_cuowu_time=self.voice_cuowu_time+1
                self.email_cuowu_time = self.email_cuowu_time + 1
            if(self.voice_cuowu_time==30):
                self.timeThread.start()
                self.voice_cuowu_time=0
            if(self.email_cuowu_time==300):
                self.timeThread1.start()
                self.email_cuowu_time=0
                    # self.zhuyemian_signal.emit()
            # if head_left==0 or head_right==0 or body_left==0 or body_right==0 or squint==0 or head_forward==0 :
            #     duration = 1000  # millisecond
            #     freq = 1440  # Hz
            #     winsound.Beep(freq, duration)
            if true_sit == 1:
                self.voice_cuowu_time=0
                self.email_cuowu_time=0
                cv2.putText(self.image, "Sit correctly", (30, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            show = cv2.resize(self.image, (640, 480))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
        else:
            self.label_show_camera.setText("未识别到图像")

    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cancel = QtWidgets.QPushButton()
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u'关闭', u'是否关闭！')
        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'确定')
        cancel.setText(u'取消')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()


if __name__ == '__main__':
    with open('D:\pythonProject5\PyQt5_yemian\结果存放', "r", encoding='utf-8') as file_obj:
        contents = file_obj.read()
        x = contents.split("-")
        yonghu_name = x[0]
        yonghu_password = x[1]  # 未完善
        print(yonghu_name)
    # conn = pymysql.connect(host='localhost', port=3306, user='root', password='nuliba520.', db='test')
    conn=sqlite3.connect('yonghu1.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? ", (yonghu_name,))
    result = cursor.fetchall()
    for row in result:
        yonghu_name = row[0]
        yonghu_password = row[1]
        yonghu_number = row[2]
        yonghu_email = row[3]
    os.remove('D:\pythonProject5\PyQt5_yemian\结果存放')
    App = QApplication(sys.argv)
    win = Ui_MainWindow()
    win.show()
    sys.exit(App.exec_())

