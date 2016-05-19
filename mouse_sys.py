
import socket

import pyautogui,math

import time
# def server():
#     address = ('192.168.31.141', 31500)
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.bind(address)
#
#     while True:
#         data, addr = s.recvfrom(2048)
#         if not data:
#             print "client has exist"
#             break
#         print "received:", data, "from", addr
#
#     s.close()



address = ('192.168.31.141', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

t=time.time()
p=0.05
lastPos=pyautogui.position()
lastTime=time.time()
c=0
while True:
    pos=pyautogui.position()
    msg=str(pos[0])+"|"+str(pos[1])
    if not msg:
        break
    px=math.fabs(pos[0]-lastPos[0])
    py=math.fabs(pos[1]-lastPos[1])
    if px>0 or py>0:
        #print msg
        s.sendto(msg, address)
        t=time.time()+p
        lastPos=pos
        #print c
        c+=1
s.close()
#
# #server()
# client()
