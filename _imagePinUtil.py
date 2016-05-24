# -*- coding: utf-8 -*-
import os,sys,wx,pyautogui,time
from _globalData import*
from PIL import Image
from  xml.etree.ElementTree import*
platform=sys.platform

# if platform=="win32":
#     #import win32ui
# elif platform=="darwin":
#     #das


# def getScreenSizeAndPos():
#     screenPS=[[0,0],[0,0]]
#     MoniterDev=win32api.EnumDisplayMonitors(None,None)
#     if len(MoniterDev)==1:
#         screenPS[0]=(MoniterDev[0][2][0],MoniterDev[0][2][1])
#         screenPS[1]=(MoniterDev[0][2][2],MoniterDev[0][2][3])
#     else:
#         ax=[]
#         ay=[]
#         bx=[]
#         by=[]
#         for s in MoniterDev:
#             ax.append(s[2][0])
#             ay.append(s[2][1])
#             ax.append(s[2][2])
#             ay.append(s[2][3])
#         screenPS[0]=(min(ax),min(ay))
#         screenPS[1]=((max(ax)-min(ax)),(max(ay)-min(ay)))
#     print "\nscrenRect: ",screenPS
#     return screenPS

def showImageInDesktop(path):
    if platform=="win32":
        os.system("explorer "+path)
    elif platform=="darwin":
        os.system("open "+path)


def removeFile(fileName):
    if os.path.isdir("backup")!=True:
        os.mkdir("backup")

    if platform=="win32":
        c="move "+fileName+" "+("backup/"+fileName)
    elif platform=="darwin":
        c="mv "+fileName+" "+("backup/"+fileName)
    else:c="error platform! on move file"
    os.system(c)

def screenCapture(savePath):
    global SAVE_SCREEN_MAP_PATH
    # hwnd = 0
    # hwndDC = win32gui.GetWindowDC(hwnd)
    # mfcDC=win32ui.CreateDCFromHandle(hwndDC)
    # saveDC=mfcDC.CreateCompatibleDC()
    # saveBitMap = win32ui.CreateBitmap()
    # saveBitMap.CreateCompatibleBitmap(mfcDC, size[0], size[1])
    # saveDC.SelectObject(saveBitMap)
    # saveDC.BitBlt((0,0),SCREEN_SIZE, mfcDC, SCREEN_POS, win32con.SRCCOPY)
    # saveBitMap.SaveBitmapFile(saveDC,SAVE_SCREEN_MAP_PATH)
    # Image.open(SAVE_SCREEN_MAP_PATH).save(SAVE_SCREEN_MAP_PATH[:-4]+".png")
    pyautogui.screenshot(SAVE_SCREEN_MAP_PATH)

def grapStart():
    global SCREEN_SIZE
    global SAVE_SCREEN_MAP_PATH
    global MAINFRAME
    mainFrame=MAINFRAME[0]
    screenCapture(SAVE_SCREEN_MAP_PATH)
    tImage=wx.Image(SAVE_SCREEN_MAP_PATH,wx.BITMAP_TYPE_PNG)
    tImage= tImage.AdjustChannels(1,1,1,0.8)
    mainFrame.bg.SetBitmap(wx.BitmapFromImage(tImage))
    mainFrame.Show()
    print "grapStart: "

def save_settings_data(mainTree,data):
    for s in data:
        if mainTree.find(s)!=None:
            if s=="ICON_PATH" or s=="SAVE_SCREEN_MAP_PATH" or s=="SET_FILE_PATH" or s=="GRAP_PF_NAME"  or s=="GRAP_PF_NAME" :
                mainTree.find(s).text=str(data[s])
            else:
                ()#mainTree.find(s).text=str(data[s])#str(data[s])
                print "xxx"
        else:
            item=Element(s)
            if s=="ICON_PATH" or  s=="SAVE_SCREEN_MAP_PATH" or s=="SET_FILE_PATH" or s=="GRAP_PF_NAME"  or s=="GRAP_PF_NAME" :
                item.text=str(data[s])#"\""+data[s].replace("\\","/")+"\""
            else:
                item.text=str(data[s])
            mainTree.append(item)

        #string
        '''
        #int
        elif s=="LANGUAGE_TYPE" or s=="IMAGE_MAX_SIZE" or s== "IMAGE_MIN_SIZE":
            data_str=str(data[s])
        #float
        elif s=="ADJUST_SCALE_SPEED" or s=="SCALE_SPEED" :
            data_str=str(data[s])
        #array
        elif s=="IMAGE_SCALE_MIN_MAX" :
            for s in data[s]:
                data_str=+str(s)+" "
        '''
        #item.text=data_str
        #mainTree.append(item)
        settings=ElementTree("root")
        settings._setroot(indent(mainTree))
        settings.write(SET_FILE_PATH,"utf-8")
        print "\n save_settings_data: "

def get_settings_data(mainTree,data):
    print "start get data: \n"
    for e in mainTree:
        s=e.tag
        try: e.text
        except:
            ()
        else:
            if s!="images":
                print e.tag,  e.text
                for n in settings_data:
                    if s==n:
                        if s=="ICON_PATH" or s=="SAVE_SCREEN_MAP_PATH" or s=="SET_FILE_PATH" or s=="GRAP_PF_NAME"  or s=="GRAP_PF_NAME" :
                            settings_data[n]=e.text
                        elif s=="IMAGE_MAX_SIZE" or s== "IMAGE_MIN_SIZE":
                            settings_data[n]=float(e.text)
                        elif s=="LANGUAGE_TYPE" :
                            settings_data[n]=int(e.text)
    print "\nget data complit! \n"

#--- indent XML string
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i
    return elem
#--- if can't find the settings file  create deflut file
def createSetingsFile():
    global ROOT_DIR
    global GRAP_PF_NAME
    main_element=Element("root")
    images_element=Element("images")
    #images_element.text="imagePin"
    files= os.listdir(ROOT_DIR)
    haveImage=False
    #print files
    for m in files:
        nameParts=os.path.basename(m).split("_")
        if nameParts[0]==GRAP_PF_NAME:
            if os.path.splitext(m)[1]==".png":
                #image_element.text=m
                haveImage=True
                images_element.append(grapPartElement(m,True,[10,10],1,m))
    settings=ElementTree("fengxx")
    main_element.append(images_element)
    settings._setroot(indent(main_element))
    settings.write(SET_FILE_PATH,"utf-8")
    print "\ncreateSetingsFile: ", SET_FILE_PATH
#--- save settings
def saveChange(mainTree,name,s,pos,sc,filePath):
    global SET_FILE_PATH
    sTree=grapPartElement(name,s,pos,str(sc),filePath)
    changeOn=False
    for s in mainTree.findall("images/image"):
        if s.find("path").text==filePath:
            s.find("path").text=sTree.find("path").text
            s.find("name").text=sTree.find("name").text
            s.find("miniState").text=sTree.find("miniState").text
            s.find("posx").text=sTree.find("posx").text
            s.find("posy").text=sTree.find("posy").text
            s.find("scale").text=sTree.find("scale").text
            changeOn=True
    if changeOn==False:
        mainTree.find("images").append(sTree)


        #for s in mainTree.findall("images/image"):
        #print  s.find("path").text,filePath
    settings=ElementTree("root")
    settings._setroot(indent(mainTree))
    settings.write(SET_FILE_PATH,"utf-8")
    #print "\nsaveChange: ",name

class textFrame(wx.Frame):
    BG_COLOR=(67,67,67)
    FG_COLOR=(120,120,120)
    SIZE=(242 ,256)
    lastPos=[0,0]
    canMove=False
    canSize=False
    mousePos=[0,0]
    minSize=[100,50]
    pos=[400,300]
    size=[0,0]
    def __init__( self, parent,id,text ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "fengx", pos = wx.DefaultPosition, size = wx.Size( 342,335 ), style = wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL )
        self.SetSizeHintsSz( wx.Size( 100,170 ), wx.DefaultSize )
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        self.SetMinSize( wx.Size( 100,20 ) )
        self.movebar = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.movebar.SetMinSize( wx.Size( 50,20 ) )
        self.movebar.SetMaxSize( wx.Size( -1,20 ) )
        bSizer1.Add( self.movebar, 1, wx.EXPAND |wx.ALL, 0 )
        self.textC = wx.TextCtrl( self, wx.ID_ANY,text, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_RICH )
        self.textC.SetMinSize( wx.Size( 70,70 ) )
        bSizer1.Add( self.textC, 6, wx.EXPAND, 0 )
        self.sizebar = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.sizebar.SetMinSize( wx.Size( 50,15 ) )
        self.sizebar.SetMaxSize( wx.Size( -1,20 ) )
        bSizer1.Add( self.sizebar, 1, wx.EXPAND |wx.ALL, 0)
        self.SetSizer( bSizer1 )
        self.Layout()
        self.Centre( wx.BOTH )
        self.sizebar.SetBackgroundColour((63,63,63))
        font = wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,False,"微软雅黑")#"Micrisoft YaHei")
        self.textC.SetFont(font)
        self.textC.SetBackgroundColour(self.BG_COLOR)
        self.textC.SetForegroundColour(self.FG_COLOR)
        self.movebar.SetBackgroundColour((59,59,59))
        self.movebar.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.movebar.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.movebar.Bind(wx.EVT_MOTION,  self.OnMove)
        self.sizebar.Bind(wx.EVT_LEFT_UP, self.OnSizeMouseLeftUp)
        self.sizebar.Bind(wx.EVT_LEFT_DOWN, self.OnSizeMouseLeftDown)
        self.sizebar.Bind(wx.EVT_MOTION,  self.OnSizeMove)


    def OnStartDrag(self, evt):
        if evt.Dragging():
            url = self.textC.GetValue()
            data = wx.URLDataObject()
            data.SetURL(url)
            dropSource = wx.DropSource(self.textC)
            dropSource.SetData(data)
            result = dropSource.DoDragDrop()
            print result,url
            f = urllib2.urlopen(url)
            with open("demo2.jpg", "wb") as code:
                code.write(f.read())

    def OnSizeMove(self, event):
        newSizeX=wx.GetMousePosition()[0]-self.lastPos[0]+self.GetClientSize()[0]
        newSizeY=wx.GetMousePosition()[1]-self.lastPos[1]+self.GetClientSize()[1]
        newSize=wx.Point=(newSizeX,newSizeY)
        if self.canSize and  self.GetClientSize()[1]>self.minSize[1] and self.GetClientSize()[0]>self.minSize[0]:
            self.SetSize(newSize)

        self.lastPos=wx.GetMousePosition()
        #self.lastPos[0]=wx.GetMousePosition()[0]
        #self.lastPos[1]=wx.GetMousePosition()[1]

    def OnSizeMouseLeftDown(self, event):
        self.sizebar.CaptureMouse()
        self.lastPos=wx.GetMousePosition()
        #self.lastPos[0]=wx.GetMousePosition()[0]
        #self.lastPos[1]=wx.GetMousePosition()[1]
        self.canSize=True


    def OnSizeMouseLeftUp(self, event):
        if self.sizebar.HasCapture():
            self.sizebar.ReleaseMouse()
        self.canSize=False
        self.b_sizenwse.SetPosition(-100,-100)
    def OnClick(self, event):
        self.log.write("Click! (%d)\n" % event.GetId())



    def OnMove(self, event):
        newPosX=event.GetPosition()[0]-self.lastPos[0]+self.pos[0]
        newPosY=event.GetPosition()[1]-self.lastPos[1]+self.pos[1]
        newPos=wx.Point=(newPosX,newPosY)
        #self.mousePos[0]=event.GetPosition()[0]
        #self.mousePos[1]=event.GetPosition()[1]
        if self.canMove:
            self.SetPosition(newPos)
            self.pos[0]=newPos[0]
            self.pos[1]=newPos[1]

    def OnMouseLeftDown(self, event):
        self.movebar.CaptureMouse()
        self.lastPos[0]=event.GetPosition()[0]
        self.lastPos[1]=event.GetPosition()[1]
        self.canMove=True

    def OnMouseLeftUp(self, event):
        if self.movebar.HasCapture():
            self.movebar.ReleaseMouse()
        self.canMove=False


def grapPartElement(n,s,p,sc,filePath):
    gpe=Element("image")
    name=Element("name")
    if n=="":
        name.text=filePath
    else:
        name.text=n

    path=Element("path")
    path.text=filePath

    miniState=Element("miniState")
    miniState.text=str(s)
    scale=Element("scale")
    scale.text=(str(sc))
    posx=Element("posx")
    posx.text=str(p[0])
    posy=Element("posy")
    posy.text=str(p[1])
    gpe.append(name)
    gpe.append(path)
    gpe.append(miniState)
    gpe.append(posx)
    gpe.append(posy)
    gpe.append(scale)
    return gpe

#createSetingsFile()
#save_settings_data(MAIN_SETTINGS_TREE,settings_data)
