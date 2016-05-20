
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
p=0.02
lastPos=pyautogui.position()
lastTime=time.time()
c=0
f=open("ms")
a=True
time.sleep(3)
while a:
    # pos=pyautogui.position()
    # msg=str(pos[0])+"|"+str(pos[1])

    if time.time()>t:
        msg= f.readline()
        if not msg or msg=="":
            a=False
            break
        print msg
        s.sendto(msg, address)
        t=time.time()+p
        #lastPos=pos
        #print c
        c+=1
s.close()
#
# #server()
# client()
