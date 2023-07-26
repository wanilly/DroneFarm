import cv2
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

from PyQt5.QtWidgets import QLabel, QLCDNumber, QGroupBox, QApplication
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QTime, QTimer
import pygame
import pandas as pd
from datetime import datetime

import keyboardcontrol as kb

#from auto import a

#rint(a) - 테스트 코드 

import pylint
pylint.run_pyreverse
pylint.version

'''

수정 중...

import ezwifi

w = ezwifi.Wifi()
w.connect("ssid", "pass")

'''

from djitellopy import tello

global d
flag = 0
d = tello.Tello()
d.connect()

class ShowVideo(QtCore.QObject):

    
    '''
    camera = cv2.VideoCapture(0)

    ret, image = camera.read()
    h, w = image.shape[:2]
         
    width = 550
    height = int(width*(h/w))
    image = cv2.resize(image, (width, height))    
    '''
    global color_swapped_image

    VideoSignal = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)
        self.parent = parent

    

    @QtCore.pyqtSlot()
    def startVideo(self):
        self.thread = QtCore.QThread()
        global image
        d.streamon()
        
        d.FPS_30
        #d.BITRATE_5MBPS

        self.frame_read = d.get_frame_read()
        #frame_read.frame
        #camera = cv2.VideoCapture(0)
        #print(camera)
        
        run_video = True
        while run_video:
            #ret, image = self.camera.read()
            
            
            image = self.frame_read.frame
            h, w = image.shape[:2]
            self.width = 500
            self.height = int(self.width* (h/w))
            image = cv2.resize(image, (self.width, self.height)) 
            #
            color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            '''
            th = 155
            gray = cv2.cvtColor(image,  cv2.COLOR_BGR2GRAY) 
            gray = cv2.inRange(gray, th, 256)
            ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            inverted_binary = cv2.bitwise_not(binary)

            black_pixels = cv2.countNonZero(inverted_binary)
            white_pixels = cv2.countNonZero(binary)
            '''
            # 이것은 흰색 픽셀 수이다. 따라서, 검정은 픽셀 수 작아지면 흰색이라고 생각하자.
            #cv2.countNonZero
            #print(hist)
            #print("b:",black_pixels, "w:", white_pixels)

            #time.sleep(1) --> 스마트 팜 내에서... -> 
            # 범위는 흰 위치, 빛에 따라 검정 , 흰 영역이 다를 것이다.

            #if black_pixels <= 90000: # and white_pixels >= 50000
                #back_button.click()
                #d.send_rc_control(0,0, -5, 0)
                #print("너무 가까워요!") # -> send_rc_command() 뒤로 10,
            
            #cv2.imwrite(color_swapped_image)
            
            qt_image1 = QtGui.QImage(color_swapped_image.data,
                                    self.width,
                                    self.height,
                                    color_swapped_image.strides[0],
                                    QtGui.QImage.Format_RGB888)
            self.VideoSignal.emit(qt_image1)
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(30, loop.quit) #25 ms
            loop.exec_()
    

    # 식물 사진 캡처할 떄 사용되는 함수
    @QtCore.pyqtSlot()
    def imgCp(self):
        self.thread = QtCore.QThread()
        cv2.imwrite(self.color_swapped_image)

# Login 사용자 확인하기
class Login(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)


# 
class Keyboard(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Keyboard, self).__init__(parent)
        self.send_update()
        global checkup
        global checkdown
        global dangerous
        global takeoff
        global manual
        global com

        com = 0

        self.rcUpdate()
        self.dangerous = False
        self.takeoff = False
    
    def rcUpdate(self):
        # 실시간 변경 성공!
        #self.dataThread = QtCore.QThread()
        #self.dataThread.start
        self.dateUpdate = QTimer()
        #self.pg = pygame.init()
        #self.pgd = pygame.display.set_mode((200, 200))
        self.dateUpdate.start(2000*1)
        self.dateUpdate.timeout.connect(self.button_center)
        
    

    def send_update(self):
        ##
        #QLabel
        #lab = QLabel(str(a))
        self.a = d.get_current_state()
        #self.a = pd.Series(self.a)
        self.dateUpdate = QTimer()
        self.dateUpdate.start(1000*1)
        self.dateUpdate.timeout.connect(self.send_update)
        #self.lab = self.QLabel(str(self.a))
        #print(str(self.a))
    
    
    
    
    def manual_control(self):
        global flag
        flag = 0
        #self.setGeometry(200, 200, 200,200)
        # 키보드 관련된 위젯들이 생겨나도록 한다.
        self.manual = False
        # 수동모드
        
        if self.manual == True:
            # 키보드로 동작하여 모든 방향 갈수 있도록 하되 장애물 그리고 범위 이상은 가지 못하도록 한다.
            print("수동모드 진행 중...") # 사용자에게 수동모드라는 것을 인식
            #return manual
        else:
            print("수동모드로 전환하세요!")
        return self.manual
    
    #
    def button_checkup(self):
        self.thread = QtCore.QThread()
        # up, down, left, right, n, m [0, ...] 모두 0으로 초기화
        
        command = 'u'
        value = kb.keyboardInput('u')
        d.send_rc_control(value[0], value[1], value[2], value[3])
       
    
    def button_center(self):
        self.thread = QtCore.QThread()
        d.send_rc_control(0, 0, 0, 0)


    def button_checkdown(self):
        self.thread = QtCore.QThread()
        # up, down, left, right, n, m [0, ...] 모두 0으로 초기화
        #if manual == True:
            #print("버튼이 눌렸다!", checkup, checkdown
        command = 'j'
        value = kb.keyboardInput('j')
        d.send_rc_control(value[0], value[1], value[2], value[3])
        self.button_center()
        return True

    def button_checkcclockwise(self):
        self.thread = QtCore.QThread()
        command = 'n'
        value = kb.keyboardInput('n')
        d.send_rc_control(value[0], value[1], value[2], value[3])
        
    
    def button_checkclockwise(self):
        self.thread = QtCore.QThread()
        command = 'm'
        value = kb.keyboardInput('m')
        d.send_rc_control(value[0], value[1], value[2], value[3])
        



    def button_checkfoward(self):
        self.thread = QtCore.QThread()
        command = 'f'
        value = kb.keyboardInput('f')
        d.send_rc_control(value[0], value[1], value[2], value[3])
        

    def button_checkback(self):
        self.thread = QtCore.QThread()
        command = 'b'
        value = kb.keyboardInput('b')
        d.send_rc_control(value[0], value[1], value[2], value[3])
        

    def button_checkleft(self):
        self.thread = QtCore.QThread()
        # up, down, left, right, n, m [0, ...] 모두 0으로 초기화
        #if manual == True:
            #print("버튼이 눌렸다!", checkup, checkdown)
        self.controller_button()
        command = 'l'
        value = kb.keyboardInput('l')
        d.send_rc_control(value[0], value[1], value[2], value[3])
        
    
    
    def button_checkright(self):
        self.thread = QtCore.QThread()
        # up, down, left, right, n, m [0, ...] 모두 0으로 초기화
        #if manual == True:
            #print("버튼이 눌렸다!", checkup, checkdown)

        command = 'r'
        value = kb.keyboardInput('r')
        d.send_rc_control(value[0], value[1], value[2], value[3])


    def button_checkm(self):
        self.thread = QtCore.QThread()
        # up, down, left, right, n, m [0, ...] 모두 0으로 초기화
        #if manual == True:
            #print("버튼이 눌렸다!", checkup, checkdown)
        command = 'm'
        value = kb.keyboardInput('m')
        d.send_rc_control(value[0], value[1], value[2], value[3])


    def button_checkstart(self):
        self.thread = QtCore.QThread()
        # up, down, left, right, n, m [0, ...] 모두 0으로 초기화
        #if manual == True:
            #print("버튼이 눌렸다!", checkup, checkdown)
        command = 's'
        kb.start('s')
        

    def button_checkland(self):
        self.thread = QtCore.QThread()
        # up, down, left, right, n, m [0, ...] 모두 0으로 초기화
        #if manual == True:
            #print("버튼이 눌렸다!", checkup, checkdown)
        #self.controller_button()
        command = 'q'
        kb.danger('q')


        
        #return checkup
            

    '''
    def button_checkdown(self):
        global checkleft
        global checkright
        global checkn
        global checkm
        global checkstart
        global checkquit
        # up, down, left, right, n, m [0, ...] 모두 0으로 초기화

        checkdown = 1
        if manual == True:
            #print("버튼이 눌렸다!", checkup, checkdown)
            return checkdown
        else:
            print("수동모드로 전환하세요!")
    '''      
    def controller_button(self):
        global command
        #kb.init()

        '''
            elif checkdown == 1:
                command = 'j'
                
                value = keyboardInput('j')
                d.send_rc_control(value[0], value[1], value[2], value[3])
        '''
    
    


# image Viewer
class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    
    def onExit(self):
        print("exit...")
        sys.exit(app.exec_())

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()
    
# 키보드모드? -수동 모드

class Manual(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Manual, self).__init__(parent)
        self.pygameinit()
        #elf.activate()


     

    def pygameinit(self):
        # 실시간 변경 성공!
        #self.dataThread = QtCore.QThread()
        #self.dataThread.start
        self.dateUpdate = QTimer()
        self.pg = pygame.init()
        self.pgd = pygame.display.set_mode((200, 200))
        self.dateUpdate.start(1000*1)
        self.dateUpdate.timeout.connect(self.pygameinit)
        # 


class WindowClass(QtWidgets.QMainWindow):
    def __init__(self):
        super( ).__init__( )
        self.setWindowTitle("실내 스마트팜 관리")
        self.setFixedSize(1000, 700)
        self.setting()
        #self.now = datetime.now()
        #self.date_print()
        self.setupUI()
        #self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
        self.dateUpdate()
        self.data_info()

    def setupUI(self):
        self.setGeometry(800, 200, 500, 300)


    def setting(self):
        global get
        get = False
        if manual_button.click() == True:
            up_button.setDisabled(False)
            down_button.setDisabled(False)
            left_button.setDisabled(False)
            right_button.setDisabled(False)

        else:
            up_button.setDisabled(False)
            down_button.setDisabled(False)
            left_button.setDisabled(False)
            right_button.setDisabled(False)

    
    def changet(self, get):
        #get = False
        get = True
            
    # data 출력하기
    def data_info(self):
        print("현재의 배터리는 @?")
        self.infoLable = QLabel()
        

    #@QtCore.pyqtSlot(QtCore.QThread)
    def dateUpdate(self):
        # 실시간 변경 성공!
        #self.dataThread = QtCore.QThread()
        #self.dataThread.start
        self.dateUpdate = QTimer()
        #self.pg = pygame.init()
        #self.pgd = pygame.display.set_mode((200, 200))
        self.dateUpdate.start(1000*1)
        self.dateUpdate.timeout.connect(self.date_print)
        
        # 

    def date_print(self):
        self.now = datetime.now().strftime('%Y.%m.%d - %H:%M:%S')
        data_str = "현재시간: " +str(self.now)

        self.sb = self.statusBar()
        self.setStatusBar(self.sb)
        self.sb.showMessage(data_str)
        self.sb.repaint()
        #self.update()
        
        '''
        push_up = QtWidgets.QPushButton('Up')ㅇ
        push_down = QtWidgets.QPushButton('Down')
        push_left = QtWidgets.QPushButton('Left')
        vertical_layout.addWidget(push_up)
        vertical_layout.addWidget(push_down)
        vertical_layout.addWidget(push_left)
        '''
        
    def drawLines(self, qp):
        pen = QPen(Qt.black, 3, Qt.SolidLine)
        self.qp.setPen(pen)
        self.qp.drawLine(50, 50, 350, 50)
        self.pen.setStyle(Qt.DashLine)
        self.qp.setPen(pen)
        self.qp.drawLine(50, 110, 350, 110)
        self.pen.setStyle(Qt.DashDotLine)
        self.qp.setPen(pen)
        self.qp.drawLine(50, 170, 350, 170)


'''
class WindowClass(QtWidgets.MainWindow):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        win = QtWidgets.QWidget()
        win.setWindowTitle('실내')
'''   
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    # add code
    win = QtWidgets.QWidget()
    vbox = QtWidgets.QVBoxLayout()
    label = QtWidgets.QLabel()
    

    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo() # show video class 불러오기
    vid.moveToThread(thread)

    image_viewer = ImageViewer()
    vid.VideoSignal.connect(image_viewer.setImage)

    #WindowClass().update()
    #s.date_print()
    # Viewer 멈추기
    ex = ImageViewer()
    
    # 수동모드 동작
    #thread2 = QtCore.QThread()
    #thread2.start()
    man = Keyboard()
    man.moveToThread(thread)
    #man.moveToThread(thread2)


    #
    
    

    # 왼쪽 버튼 생성
    leftG = QGroupBox("수동동작")
    #manual_button = 
    up_button = QtWidgets.QPushButton('위이동')
    down_button = QtWidgets.QPushButton('아래이동')
    left_button = QtWidgets.QPushButton('왼쪽이동')
    right_button = QtWidgets.QPushButton('오른쪽이동')
    countclockwise_button = QtWidgets.QPushButton('시계반대방향회전')
    clockwise_button = QtWidgets.QPushButton('시계방향회전')
    forward_button = QtWidgets.QPushButton('앞이동')
    back_button = QtWidgets.QPushButton('뒤이동')
    stop_button = QtWidgets.QPushButton('멈춤')

    takeoff_button = QtWidgets.QPushButton('takeoff')
    land_button = QtWidgets.QPushButton('land')


    # 자동 그룹
    leftG2 = QGroupBox("자동동작")
    auto_button = QtWidgets.QPushButton("auto")
    

    # 우측 버튼 생성
    rightG = QGroupBox("메인")
    start_button = QtWidgets.QPushButton('카메라시작')
    picture_button = QtWidgets.QPushButton('사진저장')
    exit_button = QtWidgets.QPushButton('Exit')
    manual_button = QtWidgets.QPushButton('Manual')
    manual_button2 = QtWidgets.QPushButton('Manual2')
    # 우측 데이터 그룹
    rightG2 = QGroupBox("데이터 정보")

    #data_button = QtWidgets.QPushButton("data")
    a = d.get_current_state()
    a = pd.Series(a)
    lab = QLabel(str(a)) #Keyboard().send_update()

    
    
    # 버튼 구성 추가
    leftInnerLayOut = QtWidgets.QVBoxLayout()
    leftInnerLayOut.addWidget(up_button)
    leftInnerLayOut.addWidget(down_button)
    leftInnerLayOut.addWidget(left_button)
    leftInnerLayOut.addWidget(right_button)

    leftInnerLayOut.addWidget(countclockwise_button)
    leftInnerLayOut.addWidget(clockwise_button)
    leftInnerLayOut.addWidget(right_button)
    #
    leftInnerLayOut.addWidget(forward_button)
    leftInnerLayOut.addWidget(back_button)
    


    leftInnerLayOut.addWidget(takeoff_button)
    leftInnerLayOut.addWidget(land_button)
    
    #leftInnerLayOut.addWidget(stop_button)


    leftG.setLayout(leftInnerLayOut)

    # 왼쪽 데이터 그룹
    leftInnerLayOut2 = QtWidgets.QVBoxLayout()
    leftInnerLayOut2.addWidget(auto_button)
    leftG2.setLayout(leftInnerLayOut2)
    
    # 왼쪽 그룹 - 안에 합치기 
    leftLayOut = QtWidgets.QVBoxLayout()
    leftLayOut.addWidget(leftG)
    leftLayOut.addWidget(leftG2)

    # 중앙 
    centerLayOut = QtWidgets.QVBoxLayout()
    #rightLayOut.addWidget(tableWidget)
    centerLayOut.addWidget(image_viewer) # -
    centerLayOut.addWidget(image_viewer) # 중앙 추가적으로 정보보여주기
    
    #
    
    
    # 오른쪽 메인 그룹
    rightInnerLayOut = QtWidgets.QVBoxLayout()
    rightInnerLayOut.addWidget(manual_button)
    rightInnerLayOut.addWidget(start_button)
    rightInnerLayOut.addWidget(picture_button)
    rightInnerLayOut.addWidget(exit_button)


    rightG.setLayout(rightInnerLayOut)
 

    rightInnerLayOut2 = QtWidgets.QVBoxLayout()
    #rightInnerLayOut2.addWidget(data_button)
    rightInnerLayOut2.addWidget(lab)
    rightG2.setLayout(rightInnerLayOut2)


    # 오른쪽 그룹
    rightLayout = QtWidgets.QVBoxLayout()
    rightLayout.addWidget(rightG)
    rightLayout.addWidget(rightG2)


    layout = QtWidgets.QHBoxLayout()
    layout.addLayout(leftLayOut)
    layout.addLayout(centerLayOut)
    layout.addLayout(rightLayout)
    #QWidget.setLayout(layout)
    


    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(layout)
    
    
    #mm = Manual()

    # clinck 연결
    
    start_button.clicked.connect(vid.startVideo)
    picture_button.clicked.connect(vid.imgCp)
    exit_button.clicked.connect(ex.onExit)
    manual_button.clicked.connect(man.manual_control)
    #manual_button.clicked.connect(k.keycontrol)
    up_button.clicked.connect(man.button_checkup)
    down_button.clicked.connect(man.button_checkdown)
    #push_left.clicked.connect(vc.value('l'))
    left_button.clicked.connect(man.button_checkleft)
    right_button.clicked.connect(man.button_checkright)

    countclockwise_button.clicked.connect(man.button_checkcclockwise)
    clockwise_button.clicked.connect(man.button_checkclockwise)
    takeoff_button.clicked.connect(man.button_checkstart)
    land_button.clicked.connect(man.button_checkland)
    forward_button.clicked.connect(man.button_checkfoward)
    back_button.clicked.connect(man.button_checkback)


    #main_window = QtWidgets.QMainWindow()
    #main_window.setCentralWidget(layout_widget)
    main_window = WindowClass()
    main_window.setCentralWidget(layout_widget)
    main_window.show()
    sys.exit(app.exec_())