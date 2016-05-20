import os,pyautogui,time,pythoncom,pyHook,socket
# def onMouseEvent(event):
#    print "MessageName:",event.MessageName
#    print "Message:", event.Message
#    #print "Time:", event.Time
#    #print "Window:", event.Window
#    #print "WindowName:", event.WindowName
#    print "Position:", event.Position
#    print "Wheel:", event.Wheel
#    #print "Injected:", event.Injected
#    #print"---"
#
#    return True

def onKeyboardEvent(event):
   print "MessageName:", event.MessageName
   print "Message:", event.Message
   print "Time:", event.Time
   print "Window:", event.Window
   print "WindowName:", event.WindowName
   print "Ascii:", event.Ascii, chr(event.Ascii)
   print "Key:", event.Key
   print "KeyID:", event.KeyID
   print "ScanCode:", event.ScanCode
   print "Extended:", event.Extended
   print "Injected:", event.Injected
   print "Alt", event.Alt
   print "Transition", event.Transition
   print "---"
   return True
   #
   # hm = pyHook.HookManager()
   # hm.KeyDown = onKeyboardEvent
   # hm.HookKeyboard()
   # hm.MouseAll = onMouseEvent
   # hm.HookMouse()
   # pythoncom.PumpMessages()

address = ('192.168.31.141', 31500)
sok = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#f=open("ms",'w')
t=40
p=0.02
s=time.time()
pp=0
mouseEvent = {"MM":512,"MLD":513,
"MLU":514,
"MRD":516,
"MRU":517,
"MMD":519,
"MMU":520,
"MW":522
}
partition_evnet=" "
def onMouseEvent(event):
    global pp
    global mouseEvent
    global s
    global t
    global f
    global p
    global sok
    global partition_evnet
    # print "MessageName:",event.MessageName
    #print "Message:", event.Message
    # print "Position:", event.Position
    # print "Wheel:", event.Wheel
    if time.time()-s>t:
        print "exit"
        #f.write("end")
        #f.close()
        exit()
    msg=""
    if event.Message==mouseEvent["MRD"]:#mouse left down
        msg=str(mouseEvent["MRD"])+partition_evnet
    elif event.Message==mouseEvent["MRU"]:
        msg=str(mouseEvent["MRU"])+partition_evnet
    elif event.Message==mouseEvent["MLD"]:
        msg=str(mouseEvent["MLD"])+partition_evnet
    elif event.Message==mouseEvent["MLU"]:
        msg=str(mouseEvent["MLU"])+partition_evnet
    elif event.Message==mouseEvent["MMD"]:
        msg=str(mouseEvent["MMD"])+partition_evnet
    elif event.Message==mouseEvent["MMU"]:
        msg=str(mouseEvent["MMU"])+partition_evnet
    elif event.Message==mouseEvent["MW"]:# mouse wheel
        msg=str(mouseEvent["MW"])+partition_evnet+str(event.Wheel)
    elif event.Message==mouseEvent["MM"]:# mouse move
        if time.time()>pp:
            pos=event.Position
            msg=str(mouseEvent["MM"])+partition_evnet+str(pos[0])+"|"+str(pos[1])
            pp=time.time()+p
    else:msg="null"
    print msg
    #f.write(msg+"\n")
    if msg!="null":
        sok.sendto(msg, address)
    return True
hm = pyHook.HookManager()
hm.MouseAll = onMouseEvent
hm.HookMouse()
pythoncom.PumpMessages()
