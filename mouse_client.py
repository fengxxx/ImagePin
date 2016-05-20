import socket,pyautogui,sys,math

from _globalData import *
from ctypes import *
address = ('192.168.31.141', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)
lastPos=pyautogui.position()
c=0
pos=(0,0)
while True:
    data, addr = s.recvfrom(100)
    if not data:
        print "client has exist"
        break
    print data
    #print "received:", data, "from", addr
    sp=data.split('|')
    #print "+++++++++",sp[0],"|",sp,"||",data
    pos=(int(sp[0]),int(sp[1]))
    #print pos
    if pos==(0,0):
        sys.exit()
    # px=math.fabs(lastPos[0]-pos[0])
    # py=math.fabs(lastPos[1]-pos[1])
    #if px>0 or py>0 :

    #pyautogui.moveTo(pos,duration=0.06)
    #pyautogui.moveTo(pos)
    windll.user32.SetCursorPos(pos[0], pos[1])
    #print c
    c+=1
    lastPos=pos

s.close()
