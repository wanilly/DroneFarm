import pygame
from time import sleep
from djitellopy import tello
import math
import time

'''
key board - 

키보드의 반응 속도가 아니라 Rc command를 보내는 시간이 걸린다.
다음 반응까지 얼마나 걸리는지 측정해봐도 좋을 듯 !! 

'''

''''
from  test4 import connect_tello
global d
d = connect_tello()
'''



dangerous = False
st = False
# parameters
foward_speed = 60/10 #117/10
degree_speed = 50/10 #360/10
interval = 0.25 #?

x = 0
y = 0
yaw = 0
dinterval = foward_speed * interval
finterval = degree_speed * interval
a = 0

d = tello.Tello()
d.connect()


def init():
    pygame.init()
    pygame.display.set_mode((200, 200))


init()

def start(command):
    global st
    if command == 's':
        print("시작합니다.")
        d.takeoff()
        st = True
    sleep(0.5)
    return st
    
def danger(command):
    global dangerous
    # 긴급 중wl
    if command == 'q':
        print("긴급 중지를 요청합니다...")
        d.land()
        dangerous = True
    
    sleep(0.5)
    return dangerous

def getkey(keyname):
    
    result = False
    for e in pygame.event.get(): pass
    keyinput = pygame.key.get_pressed()
    mykey = getattr(pygame, "K_{}".format(keyname))
    
    if keyinput[mykey]:
        result = True
        pygame.display.update()
    return result

'''

def start():
    global st
    if getkey('s'):
        print("시작합니다.")
        d.takeoff()
        st = True
    sleep(0.25)
    return st

def danger():
    global dangerous
    # 긴급 중지
    if getkey('q'):
        print("긴급 중지를 요청합니다...")
        d.land()
        dangerous = True
    sleep(0.25)
    return dangerous
'''

def keyboardInput(command):
    global yaw, x, y, a, degree
    global left_right, front_back, up_down, clock 
    left_right, front_back, up_down, clock = 0, 0, 0, 0

    # 속도도 조절해야 할까?
    speed = 15
    degree = 0
    #danger()
    global st


    if command == "l":
        getkey('LEFT') 
        left_right = -speed
        a = dinterval
        d = -180
        print("Moving Lelf")
        #print('lf', dinterval)

    elif command == "r":
        getkey('RIGHT')
        left_right = speed
        a = -dinterval
        d = 180
        print('Moving Right')

    # 앞 뒤
    if command == 'f':
        getkey('UP')
        front_back = speed
        a = dinterval
        d = 270
        print("Moving Forward")
    
    elif command == 'b':
        getkey('DOWN')
        front_back = -speed
        a = -dinterval 
        d = -90
        print("Moving Back")
    # 위로 아래로 p,l
    if command == 'u':
        getkey('u')
        up_down = speed
        print("Moving UP") 

    elif command == 'j':
        getkey('j')
        up_down = -speed
        print("Movung Down")
    
    if command == "c":
        getkey('c') 
        up_down = 0
        print("0, 0, 0, 0") 
        #print('lf', dinterval)
    # n, m /
    if command == 'n':
        getkey('n')
        clock = -speed
        yaw += finterval
        print("시계반대방향 회전 중...")

    elif command == 'm':
        getkey('m')
        clock = speed
        yaw -= finterval
        print("시계방향회전 중...")

    if start(command) == True:
        st
    if danger(command) == True:
        dangerous
    sleep(interval) #0.25
    a += yaw
    x = int(degree*math.cos(math.radians(a)))
    y = int(degree*math.sin(math.radians(a)))
    
    return [left_right, front_back, up_down, clock, x, y]



if __name__ == '__main__':
    init()
    print("초기화됨")
    while True:
        S = input('in:')
        value = keyboardInput(S)
        
        d.send_rc_control(value[0], value[1], value[2], value[3])
        #print(time.time())

'''
보낸 쪽에서 받았는지 확인!...
랜딩이나, take off시 영상 
UI 상에서 멈추는 것인지? 

프로그램의 흐름이 중요함! 

'''