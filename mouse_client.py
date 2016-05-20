import socket,pyautogui,sys,math,win32api,win32con

from _globalData import *
from ctypes import *
address = ('192.168.31.141', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)
lastPos=pyautogui.position()
c=0
pos=(0,0)
mouseEvent = {"MM":"512","MLD":"513",
"MLU":"514",
"MRD":"516",
"MRU":"517",
"MMD":"519",
"MMU":"520",
"MW":"522"
}
while True:
    data, addr = s.recvfrom(100)
    if not data:
        print "client has exist"
        #break
    msg= data.split(" ")
    if msg[0]==mouseEvent["MRD"]:#mouse left down
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0,0,0)
    elif  msg[0]==mouseEvent["MRU"]:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    elif  msg[0]==mouseEvent["MLD"]:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    elif  msg[0]==mouseEvent["MLU"]:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    elif  msg[0]==mouseEvent["MMD"]:
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN,0,0,0,0)
    elif  msg[0]==mouseEvent["MMU"]:
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP,0,0,0,0)
    elif  msg[0]==mouseEvent["MW"]:# mouse wheel
        print "xx"
        #win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,0,0)
    elif  msg[0]==mouseEvent["MM"]:# mouse move
        sp=msg[1].split('|')
        pos=(int(sp[0]),int(sp[1]))
        windll.user32.SetCursorPos(pos[0], pos[1])
        print pos
        if pos==(0,0):
            sys.exit()
    elif  msg[0]=="end":
        exit()
    else:print "null"



s.close()
