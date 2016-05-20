import os,pyautogui,time

f=open("ms",'w')

t=15

p=0.01
s=time.time()


pp=0
while time.time()-s<t:
    if time.time()>pp:
        pos=pyautogui.position()
        tempStr=str(pos[0])+"|"+str(pos[1])
        f.write(tempStr+"\n")
        pp=time.time()+p
f.close()
