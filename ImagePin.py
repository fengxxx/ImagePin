#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import win32api,win32con ,win32ui,win32gui
import wx,os,time,random,Image

from  xml.etree.ElementTree import*
from shutil import copy
from win32com.client import GetObject

helpInfor_EN='''
    ------------DESCRIPTION---------------------KEYBOARD--------------------MOSUE-----------
    |  grap  image frome screen         |   CTRL+SHIFT+ALT+A     |                         |
    |  copy image to clipboard          |   CTRL    +    C       |                         |
    |  paste image frome clipboard      |   CTRL    +    V       |                         |
    |  delete image                     |   Shift   +    Delete  |                         |
    |  delete image to backup           |   Delete               |                         |
    |  inversion image (show/hide)      |   CTRL    +    U       |                         |
    |                                   |                        |                         |
    |  hide image                       |   CTRL    +    H       |    mosue wheel kick     |
    |  image Zoom In                    |   +                    |    mouse wheel roll +   |
    |  image Zoom Out                   |   -                    |    mouse wheel roll -   |
    |  image Zoom Speed +               |   CTRL    +    +       |                         |
    |  image Zoom Speed -               |   CTRL    +    -       |                         |
    |  show help                        |   F1                   |                         |
    |                                   |                        |                         |
    |  drag image up to show it         |   PNG BMP JPG TGA      |                         |
    ----------------------------------------------------------------------------------------
 '''

helpInfor_CN='''
    |-----------DESCRIPTION-------------|-------KEYBOARD---------|----------MOSUE----------|
       从屏幕抓取图片                       CTRL+SHIFT+ALT+A                                
       复制图片到黏贴板                     CTRL    +    C                                  
       从黏贴板黏贴图片                     CTRL    +    V                                  
       删除图片(彻底删除)                   Shift   +    Delete                             
       删除图片到备份文件夹                 Delete                                          
       反向图片的(显示/隐藏)                CTRL    +    U                                  
                                                                                            
       隐藏图片                             CTRL    +    H            鼠标中键单机          
       放大图片                             +                         鼠标滚轮              
       缩小图片                             -                         鼠标滚轮              
       增加(放大/缩小)图片的速度            CTRL    +    +                                  
       减小(放大/缩小)图片的速度            CTRL    +    -                                  
       显示帮助                             F1                                              
                                                                                            
       图片文件拖上已显示的图片快速创建     PNG BMP JPG TGA                                 
    |-----------------------------------|-------------------------|-------------------------|
 '''
EN_Dic = {"grap"              :    "&Grap         -Ctrl+Shift+Alt+A",
    "save"                    :    "&Save",
    "help"                    :    "&help         -F1",
    "show"                    :    "&Show",
    "hide"                    :    "&Hide         -Ctr+H",
    "show_all_windows"        :    "Show All Window",
    "hide_all_windows"        :    "Hide All Window",
    "close"                   :    "&Close",
    "delete"                  :    "&Delete       -Delete",
    "exit"                    :    "&Exit",
    "delete_all_images"       :    "Delete All &Images",
    "show_in_explorer"        :    "Show In &Explorer",
    "reset_position"          :    "&Reset Position",
    "hide_others"             :    "Hide &Others",
    "help_infor"              :    helpInfor_EN
}
    
CN_Dic={"grap"                :    "抓取         -Ctrl+Shift+Alt+A",
    "save"                    :    "存储",
    "help"                    :    "帮助         -F1",
    "show"                    :    "显示",
    "hide"                    :    "隐藏         -Ctr+H",
    "show_all_windows"        :    "显示所有",
    "hide_all_windows"        :    "隐藏所有",
    "close"                   :    "关闭",
    "delete"                  :    "删除         -Delete",
    "exit"                    :    "退出",
    "delete_all_images"       :    "删除所有图片",
    "show_in_explorer"        :    "显示所在文件夹",
    "reset_position"          :    "复位所有图片位置",
    "hide_others"             :    "隐藏其他",
    "help_infor"              :    helpInfor_CN
}

LANGUAGE_TYPE=0

LANGUAGE_PACK_ALL=[EN_Dic,CN_Dic]
LANGUAGE_PACK=LANGUAGE_PACK_ALL[LANGUAGE_TYPE]
ROOT_DIR=os.getcwd()

ICON_PATH=ROOT_DIR+"\\app.ico"
SAVE_SCREEN_MAP_PATH=ROOT_DIR+"\\screen.png"
SET_FILE_PATH="sttings.fengx"
GRAP_PF_NAME="ThreeKindom"

CAN_GRAP=True
GRAP_RECT=[1,1,2,2]
ALL_FRAME=[]
ALL_ID=[]
MAIN_SETTINGS_TREE=ElementTree("root")
# get the screen size (support multiply display)              
SCREEN_POS=(0,0)
SCREEN_SIZE=(100,100)

SCALE_SPEED=0.1
ADJUST_SCALE_SPEED=0.04
IMAGE_MAX_SIZE=4000
IMAGE_MIN_SIZE=30
IMAGE_SCALE_MIN_MAX=[0.04,12]


settings_data={
"LANGUAGE_TYPE":LANGUAGE_TYPE,
"SCALE_SPEED":SCALE_SPEED,
 "ADJUST_SCALE_SPEED":ADJUST_SCALE_SPEED,
"IMAGE_MAX_SIZE":IMAGE_MAX_SIZE,
"IMAGE_MIN_SIZE":IMAGE_MIN_SIZE,
"IMAGE_SCALE_MIN_MAX":IMAGE_SCALE_MIN_MAX ,
"ICON_PATH":ROOT_DIR,
"SAVE_SCREEN_MAP_PATH":SAVE_SCREEN_MAP_PATH,
"SET_FILE_PATH":SET_FILE_PATH,
"GRAP_PF_NAME":GRAP_PF_NAME
}

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window,pos):
        wx.FileDropTarget.__init__(self)
        self.window = window
        self.pos=[pos[0],pos[1]]
    def OnDropFiles(self, x, y, filenames):
        i=0
        for f in filenames:
            fileE=os.path.splitext(f)[1]
            file_types=[".png",".PNG",".jpg",".JPG",".tga",".TGA",".bmp",".BMP"]
            for s in file_types:
                if fileE==s:
                    i+=1
                    im = Image.open(f)
                    mapName="ThreeKindom_"+str(i)+"_"+str(int(time.time()))+".png"
                    im.save(mapName,format="png")
                    print "import  image  succeed: " ,f
                    createMap(mapName,True,[self.pos[0]*0.33,self.pos[1]*0.33],1)
                else:
                    print "import image  failure: ",f

#get screnPos and max size
def getScreenSizeAndPos():
    screenPS=[[0,0],[0,0]]
    MoniterDev=win32api.EnumDisplayMonitors(None,None)    
    if len(MoniterDev)==1:
        screenPS[0]=(MoniterDev[0][2][0],MoniterDev[0][2][1])
        screenPS[1]=(MoniterDev[0][2][2],MoniterDev[0][2][3])        
    else:
        ax=[]
        ay=[]
        bx=[]
        by=[]
        for s in MoniterDev:
            ax.append(s[2][0])
            ay.append(s[2][1])
            ax.append(s[2][2])
            ay.append(s[2][3]) 
        screenPS[0]=(min(ax),min(ay))
        screenPS[1]=((max(ax)-min(ax)),(max(ay)-min(ay)))
    return screenPS

#  -------------- xml
def grapPartElement(n,s,p,sc):
    gpe=Element(n)
    name=Element("name")
    name.text=n
    miniState=Element("miniState")
    miniState.text=str(s)
    scale=Element("scale")
    scale.text=(str(sc))
    posx=Element("posx")
    posx.text=str(p[0])
    posy=Element("posy")
    posy.text=str(p[1])
    gpe.append(name)
    gpe.append(miniState)
    gpe.append(posx)
    gpe.append(posy)
    gpe.append(scale)
    return gpe

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
    item=Element("root")
    t=Element("images")
    files= os.listdir(ROOT_DIR)
    #fElement=[]
    for m in files:
        nameParts=os.path.basename(m).split("_") 
        if nameParts[0]==GRAP_PF_NAME:
            if os.path.splitext(m)[1]==".png":
                t.append(grapPartElement(m,True,[10,10],1))
    settings=ElementTree("fengxx")
    item.append(t)
    settings._setroot(indent(item))
    settings.write(SET_FILE_PATH,"utf-8")

#--- save settings
def saveChange(mainTree,name,s,pos,sc):
    global SET_FILE_PATH
    sTree=grapPartElement(name,s,pos,str(sc))
    if mainTree.find("images").find(name)!=None:
        mainTree.find("images").remove(mainTree.find("images").find(name))
    mainTree.find("images").append(sTree)
    settings=ElementTree("root")
    settings._setroot(indent(mainTree))
    settings.write(SET_FILE_PATH,"utf-8")

def get_settings_data(mainTree,data):
    for e in mainTree:
        s=e.tag
        if s!="images":
            print (s+"="+e.text)
            exec((s+"="+e.text))
    print "LANGUAGE_TYPE",LANGUAGE_TYPE
'''
        if s=="ICON_PATH" or s=="SAVE_SCREEN_MAP_PATH" or s=="SET_FILE_PATH" or s=="GRAP_PF_NAME"  or s=="GRAP_PF_NAME" :
            
            exec((s+"="+e.text))
        #int
        elif s=="LANGUAGE_TYPE" or s=="IMAGE_MAX_SIZE" or s== "IMAGE_MIN_SIZE":
            exec((s+"="+e.text))
        #float
        elif s=="ADJUST_SCALE_SPEED" or s=="SCALE_SPEED" :
            exec((s+"="+e.text))
        #array
        elif s=="IMAGE_SCALE_MIN_MAX" :  
            exec((s+"="+e.text))
        '''
        
def save_settings_data(mainTree,data):
    global LANGUAGE_TYPE
    for s in data:
        if mainTree.find(s)!=None:
            exec(("a="+s))
            if s=="ICON_PATH" or s=="SAVE_SCREEN_MAP_PATH" or s=="SET_FILE_PATH" or s=="GRAP_PF_NAME"  or s=="GRAP_PF_NAME" :
                exec(("a="+s))
                #print "a",a
                mainTree.find(s).text="\""+a+"\""#"\""+data[s].replace("\\","/")+"\""
                # print "str: ",mainTree.find(s).text
            else:
                mainTree.find(s).text=str(a)#str(data[s])
                # print s , (data[s])
                # print "ect: ",mainTree.find(s).text
        else:
            item=Element(s)
            if s=="ICON_PATH" or  s=="SAVE_SCREEN_MAP_PATH" or s=="SET_FILE_PATH" or s=="GRAP_PF_NAME"  or s=="GRAP_PF_NAME" :
                item.text="\""+data[s].replace("\\","/")+"\""
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
class helpFrame(wx.Frame):
    global LANGUAGE_TYPE,MAIN_SETTINGS_TREE ,settings_data
   
    def __init__(self, parent,id):
        global LANGUAGE_TYPE
        helpSize=(900,300)
        windowSize=(helpSize[0],(helpSize[1]+120))
        wx.Frame.__init__(self, parent, id, 'ImagePin_help', size=windowSize,style=wx.DEFAULT_FRAME_STYLE)
        self.SetBackgroundColour((67,67,67))
        self.main_P=wx.Panel(self)
        help_text=wx.StaticText(self.main_P, -1, LANGUAGE_PACK["help_infor"], pos=(0,0),size=helpSize)
        font = wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL)
        help_text.SetFont(font)
        help_text.SetForegroundColour((130,130,130))

        self.b_CN = wx.RadioButton(self.main_P, -1, u"Chinese 中文",(300, (helpSize[1]+20)), (150, 20), style = wx.RB_GROUP )
        self.b_EN = wx.RadioButton(self.main_P, -1, u"English 英文",(450, (helpSize[1]+20)), (150, 20), style = wx.RB_GROUP )
  

        grid = wx.FlexGridSizer( cols=2 )
        box1_title = wx.StaticBox( self.main_P, -1, " " )
        box1 = wx.StaticBoxSizer( box1_title, wx.VERTICAL, )
        grid2 = wx.FlexGridSizer( cols=2 )
        grid.Add( self.b_CN, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 0 )
        grid.Add( self.b_EN, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 0 )
        box1.Add( grid, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
        box1.Add( help_text, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
        self.Bind(wx.EVT_RADIOBUTTON, self.OnGroup1Select, self.b_EN ) 
        self.Bind(wx.EVT_RADIOBUTTON, self.OnGroup1Select, self.b_CN )
        self.main_P.SetSizer(box1)
        box1.Fit( self.main_P )
        

        
        if LANGUAGE_TYPE==1:
            self.b_EN.SetValue(0)
            self.b_EN.SetValue(1)
        else:
            self.b_EN.SetValue(1)
            self.b_EN.SetValue(0)         
  
  
    def OnGroup1Select( self, event ):
        global LANGUAGE_TYPE
        radio_selected = event.GetEventObject()
        #radio_selected.Enable=False
        if self.b_CN is radio_selected:
            self.b_EN.SetValue(0)
            LANGUAGE_TYPE=1
            print "LANGUAGE_TYPE: ",LANGUAGE_TYPE
        elif self.b_EN is radio_selected:
            self.b_CN.SetValue(0)
            LANGUAGE_TYPE=0
            print "LANGUAGE_TYPE: ",LANGUAGE_TYPE
        save_settings_data(MAIN_SETTINGS_TREE,settings_data)
# tabbar icon class
class TB_Icon(wx.TaskBarIcon):
    global ICON_PATH
    global ALL_FRAME
    global settings_data
    m_close=wx.NewId()
    m_seting=wx.NewId()
    m_hide=wx.NewId()
    m_show=wx.NewId()
    m_screenGrap=wx.NewId()
    m_DeleteAll=wx.NewId()
    m_reset=wx.NewId()
    m_frameManager=wx.NewId()
    m_showInExplorer=wx.NewId()
    m_help=wx.NewId()
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon( wx.Icon(ICON_PATH, wx.BITMAP_TYPE_ICO), "screenGrap by fengx!")
        self.imgidx = 1

        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarActivate )   
        self.Bind(wx.EVT_MENU, self.showALL_FRAME, id=self.m_show)
        self.Bind(wx.EVT_MENU, self.hideALL_FRAME, id=self.m_hide) 
        self.Bind(wx.EVT_MENU, self.grapScreen, id=self.m_screenGrap)
        self.Bind(wx.EVT_MENU, self.closeApp, id=self.m_close)
        self.Bind(wx.EVT_MENU, self.onDeleteAll, id=self.m_DeleteAll)
        self.Bind(wx.EVT_MENU, self.reset, id=self.m_reset)
        self.Bind(wx.EVT_MENU, self.frameManager,id=self.m_frameManager)
        self.Bind(wx.EVT_MENU, self.showInExplorer,id=self.m_showInExplorer)
        self.Bind(wx.EVT_MENU, self.showHelp,id=self.m_help)
    def CreatePopupMenu(self):
    
        
        menu= wx.Menu()
        menu.Append(self.m_help,LANGUAGE_PACK["help"])
        #menu.Append(self.m_frameManager,"FrameManager")
        menu.Append(self.m_showInExplorer, LANGUAGE_PACK["show_in_explorer"])
        menu.Append(self.m_show, LANGUAGE_PACK["show_all_windows"]) 
        menu.Append(self.m_hide,  LANGUAGE_PACK["hide_all_windows"])
        menu.Append(self.m_reset,LANGUAGE_PACK["reset_position"])
        menu.AppendSeparator()
        menu.Append(self.m_screenGrap, LANGUAGE_PACK["grap"])
        menu.Append(self.m_DeleteAll, LANGUAGE_PACK["delete_all_images"])
        menu.Append(self.m_close, LANGUAGE_PACK["exit"])
        return menu


    def OnTaskBarActivate(self, evt):
        grapStart(bmp)
        '''
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()
        '''
    def OnTaskBarClose(self, evt):
        self.frame.Show(False)

    def OnTaskBarChange(self, evt):
        self.SetIcon(wx.Icon(os.getcwd()+'\\arp.ico'), "This is a new icon: " + name)
        #self.frame.Show(True)
        
    def showHelp(self,evt):
        newFrame = helpFrame(parent=None,id=0)
        newFrame.Show()
    def reset(self,evt):
        i=0
        for s in ALL_FRAME:
            i+=1
            try:
                #s.show()
                a=1
                s.scale=0.4
                
                s.pos=[i*15,i*15]
                s.miniState=False
                s.SetPosition(s.pos)
                s.resizeMap(s.scale)
            except :
                ()
        #os.remove(SET_FILE_PATH)

        #MAIN_SETTINGS_TREE=Element(" ")
        #start()
    def showALL_FRAME(self,evt):
        for s in ALL_FRAME:
            try:
                s.Show()
            except ImportError:
                ()
    def hideALL_FRAME(self,evt):
        for s in ALL_FRAME:   
            try:
                s.Hide()
            except ImportError:
                ()
    def closeApp(self, evt):
        for s in ALL_FRAME:
            try:
                s.saveData()
            except:
                ()
        save_settings_data(MAIN_SETTINGS_TREE,settings_data)
        self.RemoveIcon()
        #self.frame.Close()
        if os.path.isfile("screen.png"):
        	os.remove("screen.png")
        os.system("taskkill /f /im  ImagePin.exe &exit()")
        sys.exit()
    def showInExplorer(self, evt):
        os.popen("explorer "+os.getcwd())

    def grapScreen(self, evt):
        grapStart(bmp)

    def onDeleteAll(self, event):
        global ROOT_DIR
        global ALL_FRAME
        files= os.listdir(ROOT_DIR)
        
        dlg = wx.MessageDialog(None, u"are you sure to delete all data\nis can't undo", u"Delete all data", wx.YES_NO | wx.ICON_QUESTION)  
        if dlg.ShowModal() == wx.ID_YES:  
            #self.Close(True)
            #MAIN_SETTINGS_TREE.remove()
            #saveChange()
            for s in ALL_FRAME:
                try:
                    s.Hide()
                    s.Close()
                except ImportError:
                    ()
            for s in ALL_FRAME:
                try:
                    s.Hide()
                    s.Close()
                except ImportError:
                    ()
            for m in files:
                if os.path.splitext(m)[1]==".png":
                    if os.path.isdir("backup")!=True:
                        os.mkdir("backup")
                    c="move "+m+" " + ".\\backup\\" + os.path.split(m)[1]
                    os.system(c)


        ALL_FRAME=[]
        dlg.Destroy()  
    def frameManager(self,event):
        FM=frameManage(parent=None,id=-1)
        FM.Show()


class frameManage(wx.Frame):
    global SCREEN_SIZE
    global ALL_FRAME
    global curName
    #global MAIN_SETTINGS_TREE
    def __init__(self, parent, id):
        global curName
        global ALL_FRAME
        global ALL_ID
        global SCREEN_SIZE
        wx.Frame.__init__(self, parent, id,'null',size=[820,((len(ALL_FRAME)/8+1)*100+30)],pos=[100,100]) #,style=wx.STAY_ON_TOP
        tBmp=wx.EmptyBitmap(100,100, depth=-1) 
        bCount=[8,8]
        bSize=100
        frameSize=[100,100]
        i=0
        for s in ALL_FRAME:
            tempPos=[(i-(i/bCount[0]*bCount[0]))*bSize,(i/bCount[0])*bSize]
            
            self.b = wx.ToggleButton(self, -1,s.name,style=3, pos=tempPos,size=frameSize)#[200,200])
            self.b.SetValue(s.miniState)
            #self.b.SetBackgroundColour((176,176,176))
            #self.b.SetForegroundColour((150,0,0))
            #print self.b.GetBackgroundStyle()
            #if i<3:
            #    self.b.SetBackgroundStyle(i)
            #if s.miniState:
            #     self.b.SetBackgroundColour((0,255,0))
            #self.b.SetOwnBackgroundColour((0,255,0))
            #print 
            #self.b.Enable=s.miniState
            ALL_ID.append(self.b.GetId())
            
            tImage=wx.Image(s.name,wx.BITMAP_TYPE_PNG)
            newSize=[bSize,bSize]
            if tImage.Width-tImage.Height>0:
                newSize=[bSize,int(tImage.Height/(tImage.Width/(bSize+0.0)))]
            else:
                newSize=[int(tImage.Width/(tImage.Height/(bSize+0.0))),bSize]
            tImage.Rescale(newSize[0],newSize[1])
            self.b.SetBitmap(wx.BitmapFromImage(tImage))
            #print dir(self.b)
            #self.b.SetInitialSize() 
            i+=1

            self.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggle, self.b)

    def OnToggle(self,event):
        i=0
        for s in ALL_ID:
            if event.GetId()==s:
                if event.Checked():
                    ALL_FRAME[i].Show()
                    #self.SetBackgroundColour((255,255,255))
                    #print dir(event)
                else:
                    ALL_FRAME[i].Hide()
                    #self.SetBackgroundColour((0,255,0))
            i+=1
        

class DragShape:
    def __init__(self, bmp):
        self.bmp = bmp
        self.pos = (0,0)
        self.shown = True
        self.text = None
        self.fullscreen = False

    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)

    def GetRect(self):
        return wx.Rect(self.pos[0], self.pos[1],
                      self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op = wx.COPY):
        if self.bmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)

            dc.Blit(self.pos[0], self.pos[1],
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)

            return True
        else:
            return False
            
class TestPanel(wx.Panel):
    def __init__(self,parent):
        #self.log = log
        wx.Panel.__init__(self, parent, -1)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        txt = """\
If this build of wxPython includes the new wx.GCDC class (which
provides the wx.DC API on top of the new wx.GraphicsContext class)
then these squares should be transparent.
"""
        wx.StaticText(self, -1, txt, (20, 20))
        

    def OnPaint(self, evt):
        pdc = wx.PaintDC(self)
        try:
            dc = wx.GCDC(pdc)
        except:
            dc = pdc
        rect = wx.Rect(0,0, 100, 100)
        for RGB, pos in [((178,  34,  34), ( 50,  90)),
                         (( 35, 142,  35), (110, 150)),
                         ((  0,   0, 139), (170,  90))
                         ]:
            r, g, b = RGB
            penclr   = wx.Colour(r, g, b, wx.ALPHA_OPAQUE)
            brushclr = wx.Colour(r, g, b, 128)   # half transparent
            dc.SetPen(wx.Pen(penclr))
            dc.SetBrush(wx.Brush(brushclr))
            rect.SetPosition(pos)
            dc.DrawRoundedRectangleRect(rect, 8)

        # some additional testing stuff
        #dc.SetPen(wx.Pen(wx.Colour(0,0,255, 196)))
        #dc.SetBrush(wx.Brush(wx.Colour(0,0,255, 64)))
        #dc.DrawCircle(50, 275, 25)
        #dc.DrawEllipse(100, 275, 75, 50)
        
          
            
class grapingScreenFrame(wx.Frame):
    global ICON_PATH
    global SCREEN_SIZE
    global MAIN_SETTINGS_TREE
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id,'ImagePin',size=SCREEN_SIZE,style=wx.NO_BORDER|wx.STAY_ON_TOP|wx.FRAME_NO_TASKBAR)
        tBmp=wx.EmptyBitmap(600,600, depth=-1)
        self.SetSize(SCREEN_SIZE)
        #self.bg=wx.Panel(self,size=SCREEN_SIZE,id=-1)
        #self.bg.Bind(wx.EVT_PAINT, self.OnPaint)
        # wx.Frame.__init__(self, parent, id, 'fengxEngine', size=(585, 405),style=wx.DEFAULT_FRAME_STYLE)
        # self.SetBackgroundColour((100,250,205))
        # self.p= TestPanel(self)
        # txt = """\
# If this build of wxPython includes the new wx.GCDC class (which
# provides the wx.DC API on top of the new wx.GraphicsContext class)
# then these squares should be transparent.
# """
        # wx.StaticText(self, -1, txt, (20, 20))
        #self.bmp = wx.Image("ThreeKindom_1_1410689213.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        #self.b=wx.StaticBitmap(self.a, -1, bmp, (10, 20))
        
        self.bg=wx.StaticBitmap(self,-1,  tBmp, (0,0))
        self.bg.Bind(wx.EVT_LEFT_UP, self.OnLeftMouseUp)
        self.bg.Bind(wx.EVT_LEFT_DOWN, self.OnLeftMouseDown)
        self.bg.Bind(wx.EVT_MIDDLE_UP,  self.close)
        self.bg.Bind(wx.EVT_RIGHT_DOWN,  self.close)
        
        #self.a=wx.Panel(self,size=(1200,900))
        #self.bce=wx.Button(self.bg, -1, label=u'Enter') 
        self.icon = wx.Icon(ICON_PATH, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)  
        self.SetPosition(SCREEN_POS)
        '''
        self.shapes=[]
        grap_box_bmp=wx.EmptyBitmap(50,50, depth=-1)
        self.drag_box_start=DragShape(grap_box_bmp)
        self.drag_box_start.pos = (5, 5)
        self.drag_box_start.fullscreen = True
        self.shapes.append(self.drag_box_start)
        #self.drag_box_end=DragShape(grap_box_bmp)
        '''

        #set icon
        try:
            self.tbicon = TB_Icon(self)
        except:
            self.tbicon = None
        '''
        
    def OnPaint(self, evt):
        pdc = wx.PaintDC(self)
        try:
            dc = wx.GCDC(pdc)
        except:
            dc = pdc
        rect = wx.Rect(0,0, 100, 100)
        for RGB, pos in [((178,  34,  34), ( 50,  90)),
                         (( 35, 142,  35), (110, 150)),
                         ((  0,   0, 139), (170,  90))
                         ]:
            r, g, b = RGB
            penclr   = wx.Colour(r, g, b, wx.ALPHA_OPAQUE)
            brushclr = wx.Colour(r, g, b, 128)   # half transparent
            dc.SetPen(wx.Pen(penclr))
            dc.SetBrush(wx.Brush(brushclr))
            rect.SetPosition(pos)
            dc.DrawRoundedRectangleRect(rect, 8)
            
        # some additional testing stuff
        dc.SetPen(wx.Pen(wx.Colour(0,0,255, 196)))
        dc.SetBrush(wx.Brush(wx.Colour(0,0,255, 64)))
        dc.DrawCircle(50, 275, 25)
        dc.DrawEllipse(100, 275, 75, 50)
    def xxOnPaint(self, evt):
        #p=evt.GetPosition()

        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush("WHITE"))
        dc.Clear()

        dc.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD, True))
        dc.DrawText("Bitmap alpha blending (on all ports but gtk+ 1.2)",25,25)
        bmp =wx.BitmapFromImage(wx.Image("ThreeKindom_1_1410689213.png",wx.BITMAP_TYPE_PNG))
        
        if "gtk1" in wx.PlatformInfo:
            # Try to make up for lack of alpha support in wxGTK (gtk+
            # 1.2) by converting the alpha blending into a
            # transparency mask.

            # first convert to a wx.Image
            img = bmp.ConvertToImage()

            # Then convert the alpha channel to a mask, specifying the
            # threshold below which alpha will be made fully
            # transparent
            img.ConvertAlphaToMask(220)

            # convert back to a wx.Bitmap
            bmp = img.ConvertToBitmap()

            
        dc.DrawBitmap(bmp, 25,100, True)

        dc.SetFont(self.GetFont())
        y = 75
        for line in range(10):
            y += dc.GetCharHeight() + 5
            dc.DrawText("xxx", 200, y)
        dc.DrawBitmap(bmp, 0,0, True)
        
      '''  
    def OnLeftMouseDown(self, event):
        GRAP_RECT[0]= event.GetPosition()[0]
        GRAP_RECT[1]= event.GetPosition()[1]
    
            
    def OnLeftMouseUp(self, event):
        GRAP_RECT[2]= event.GetPosition()[0]
        GRAP_RECT[3]= event.GetPosition()[1]
        
        minSize=45
        if abs(GRAP_RECT[3]-GRAP_RECT[1])>=minSize and abs(GRAP_RECT[2]-GRAP_RECT[0])>=minSize: 
            grap(GRAP_RECT)
            self.Hide()
        
    def close(self,event):
        self.Hide()
    
class grapPartFrame(wx.Frame):
    global SCREEN_SIZE
    global SCREEN_POS
    global SCALE_SPEED
    global ADJUST_SCALE_SPEED
    global IMAGE_MAX_SIZE
    global IMAGE_MIN_SIZE
    global LANGUAGE_TYPE
    name=""
    miniState=False
    pos=SCREEN_POS
    mousePos=[0,0]
    scale=1
    lastPos=[0,0]
    canMove=False
    bSize=SCREEN_SIZE
    sSize=(SCREEN_SIZE[0]*0.1,SCREEN_SIZE[1]*0.1)
    log="ss"
    ID=0
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'fengx', size=SCREEN_SIZE,style=wx.NO_BORDER|wx.STAY_ON_TOP|wx.FRAME_NO_TASKBAR|wx.FRAME_SHAPED)
        tBmp=wx.EmptyBitmap(600,600, depth=-1)
        self.bg=wx.StaticBitmap(self,-1,  tBmp, (0,0))
        self.bg.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.bg.Bind(wx.EVT_LEFT_DCLICK, self.OnMouseLeftDclick)
        self.bg.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.bg.Bind(wx.EVT_MOTION,  self.OnMove)
        self.bg.Bind(wx.EVT_MIDDLE_UP,  self.onHide)
        self.Bind(wx.EVT_MOUSEWHEEL, self.scaleMap)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        self.Bind(wx.EVT_KEY_DOWN,self.OnKeyDown)
        self.bg.SetDropTarget( MyFileDropTarget(self.bg,SCREEN_SIZE) ) 

    '''
    def SetWindowShape(bbmp):
        bmp=bbmp
        if wx.Platform != "__WXMAC__":
            # wxMac clips the tooltip to the window shape, YUCK!!!
            self.SetToolTipString("Right-click to close the window\n"
                                  "Double-click the image to set/unset the window shape")

        if wx.Platform == "__WXGTK__":
            # wxGTK requires that the window be created before you can
            # set its shape, so delay the call to SetWindowShape until
            # this event.
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetWindowShape)
        else:
            # On wxMSW and wxMac the window has already been created, so go for it.
            self.SetWindowShapeFromBmp(bbmp)
    '''

    def SetWindowShape(self, bbmp):
        r = wx.RegionFromBitmap(bbmp)
        self.hasShape = self.SetShape(r)
        if wx.Platform != "__WXMAC__":
            # wxMac clips the tooltip to the window shape, YUCK!!!
            self.SetToolTipString("Right-click to close the window\n"
                                  "Double-click the image to set/unset the window shape")

        if wx.Platform == "__WXGTK__":
            # wxGTK requires that the window be created before you can
            # set its shape, so delay the call to SetWindowShape until
            # this event.
            #self.Bind(wx.EVT_WINDOW_CREATE, self.SetWindowShape)
            print "hai mei xie wang!"
        else:
            # On wxMSW and wxMac the window has already been created, so go for it.
           

            # Use the bitmap's mask to determine the region
            self.dc = wx.ClientDC(self)

            self.dc.DrawBitmap(bbmp, 0,0, True)

    def resizeMap(self,sc):
        im=wx.Image(self.name)
        size=im.GetSize()
        maxPix=min(size)*self.scale
        minPix=min(size)*self.scale
        
        if (self.scale>1 and  maxPix>IMAGE_MAX_SIZE) or (self.scale<1 and  minPix<IMAGE_MIN_SIZE):
            ()
        else:
            tSize=(size[0]*self.scale,size[1]*self.scale)
            tim=im.Rescale(size[0]*self.scale,size[1]*self.scale)
            self.bg.SetBitmap(wx.BitmapFromImage(tim))  
            self.SetSize(tSize)  
            self.SetWindowShape(wx.BitmapFromImage(tim))

    def scaleMap(self,event):
        global SCREEN_SIZE
        im=wx.Image(self.name)
        size=im.GetSize()
        if event.GetWheelRotation()<0:
            if  self.scale*size[0]>IMAGE_MIN_SIZE and self.scale*size[1]>IMAGE_MIN_SIZE:
                self.scale=self.scale*(1-SCALE_SPEED)
                self.resizeMap(self.scale)
        else: 
            if  self.scale*size[0]< SCREEN_SIZE[0]*1.4 and self.scale*size[1]< SCREEN_SIZE[1]*1.4:
                self.scale=self.scale*(1+SCALE_SPEED)
                self.resizeMap(self.scale)


    def OnMouseLeftDclick(self, event):  
        im=wx.Image(self.name) 
        newSize=(50,50)
        minSize=60.0
        minScale=1
        mapSize=(im.Width,im.Height)
        if self.GetSize()[0]<=minSize or self.GetSize()[1]<=minSize:
            tim=im.Rescale(im.Width,im.Height)
            self.bg.SetBitmap(wx.BitmapFromImage(tim))  
            self.SetSize((im.Width,im.Height))
            newPos=[int(self.pos[0]+event.GetPosition()[0]-mapSize[0]/2),int(self.pos[1]+event.GetPosition()[1]-mapSize[1]/2)]
            self.SetPosition(newPos)
            self.pos=newPos
            self.scale=1
            
        else:
            if im.Width>=im.Height:
                minScale=minSize/im.Height
                newSize=(int(im.Width*minScale),int(minSize))
            else:
                minScale=minSize/im.Width
                newSize=(int(minSize),int(im.Height*minScale))

            tim=im.Rescale(int(im.Width*minScale),int(im.Height*minScale))
            self.bg.SetBitmap(wx.BitmapFromImage(tim))  
            self.SetSize(newSize)
            newPos=[int(self.pos[0]+event.GetPosition()[0]-minSize/2),int(self.pos[1]+event.GetPosition()[1]-minSize/2)]#[int(self.pos[0]+mapSize[0]/2),int(self.pos[1]+mapSize[1]/2)]
            self.SetPosition(newPos)

            self.pos=newPos
            self.scale=minScale
            self.saveData()
        #z,g,b,a = Image(self.name).split()
        #print a
        self.SetWindowShape(wx.BitmapFromImage(tim))
    def OnMouseLeftDown(self, event):
        self.lastPos[0]=event.GetPosition()[0]
        self.lastPos[1]=event.GetPosition()[1]
        self.canMove=True


    def OnMouseLeftUp(self, event):
        self.canMove=False
        #self.saveData()

    def close(self,event):
        self.Close()

    def OnMouseRightDown(self, event):
        print "RightDown"
        #self.Close()

    def OnMove(self, event):
        newPosX=event.GetPosition()[0]-self.lastPos[0]+self.pos[0]
        newPosY=event.GetPosition()[1]-self.lastPos[1]+self.pos[1]
        newPos=wx.Point=(newPosX,newPosY)
        self.mousePos[0]=event.GetPosition()[0]
        self.mousePos[1]=event.GetPosition()[1]
        if self.canMove:
            self.SetPosition(newPos)
            self.pos[0]=newPos[0]
            self.pos[1]=newPos[1]

    def OnContextMenu(self, event):
        # only do this part the first time so the events are only bound once
        #
        # Yet another anternate way to do IDs. Some prefer them up top to
        # avoid clutter, some prefer them close to the object of interest
        # for clarity. 

        if not hasattr(self, "pp_SAVE"):
            self.pp_SAVE = wx.NewId()
            self.pp_CLOSE = wx.NewId()
            self.pp_HIDE = wx.NewId()
            self.pp_DELETE = wx.NewId()
            self.pp_TEST= wx.NewId()
            self.pp_GRAP=wx.NewId()
            self.pp_HIDE_OTHER= wx.NewId()
            self.pp_SHOW_ALL=wx.NewId()
            self.pp_FRAMEMANAGER=wx.NewId()
            self.pp_SHOWINEXPLORER=wx.NewId()
            self.Bind(wx.EVT_MENU, self.hideOther_FRAME, id=self.pp_HIDE_OTHER)
            self.Bind(wx.EVT_MENU, self.showALL_FRAME, id=self.pp_SHOW_ALL)

            self.Bind(wx.EVT_MENU, self.onSave, id=self.pp_SAVE)
            self.Bind(wx.EVT_MENU, self.onClose, id=self.pp_CLOSE)
            self.Bind(wx.EVT_MENU, self.onHide, id=self.pp_HIDE)
            self.Bind(wx.EVT_MENU, self.onDelete, id=self.pp_DELETE)    
            self.Bind(wx.EVT_MENU, self.grapScreen, id=self.pp_GRAP)
            self.Bind(wx.EVT_MENU, self.showFrameManager, id=self.pp_FRAMEMANAGER)
            self.Bind(wx.EVT_MENU, self.showInExplorer, id=self.pp_SHOWINEXPLORER)
        
        
        
        menu = wx.Menu()
        menu.Append(self.pp_GRAP,LANGUAGE_PACK["grap"])
        item = wx.MenuItem(menu, self.pp_SAVE,LANGUAGE_PACK["save"])
        bmp=wx.BitmapFromIcon(wx.Icon(os.getcwd()+'\\App.ico'))
        menu.AppendItem(item)
        #menu.Append(self.pp_FRAMEMANAGER,"&Show Frame Manager")
        menu.Append(self.pp_SHOWINEXPLORER, LANGUAGE_PACK["show_in_explorer"])
        menu.Append(self.pp_HIDE_OTHER, LANGUAGE_PACK["hide_others"])
        menu.Append(self.pp_SHOW_ALL, LANGUAGE_PACK["show_all_windows"])

        menu.Append(self.pp_CLOSE, LANGUAGE_PACK["close"])
        menu.Append(self.pp_HIDE, LANGUAGE_PACK["hide"])
        menu.Append(self.pp_DELETE, LANGUAGE_PACK["delete"])

        self.PopupMenu(menu)
        menu.Destroy()

    def grapScreen(self, evt):
        grapStart(bmp)

    def onSave(self,event):
        wildcard = "png (*.png)|*.png|bmp (*.bmp)|*.bmp|tga (*.tga)|*.tga|jpg (*.jpg)|*.jpg|"     \
        "All files (*.*)|*.*"
        dialog=wx.FileDialog(self, message="Save file as ...", defaultDir=os.getcwd(), 
        defaultFile=self.name, wildcard=wildcard,style=wx.SAVE)
        tPath=os.path.dirname(self.name) 
        tPath=ROOT_DIR+"\\"+self.name
        if dialog.ShowModal()==wx.ID_OK:
            im = Image.open(self.name)
            file_et=os.path.splitext(dialog.GetPath())[1]
            im.save(dialog.GetPath(),format=file_et)
        dialog.destory()
    def onClose(self, event):
        ALL_FRAME.remove(self)
        self.saveData()
        self.Close()

    def onHide(self, event):
        self.miniState=False
        self.saveData()
        self.Hide()

    def onDelete(self, event):
        global  ALL_FRAME
        ALL_FRAME.remove(self)
        if os.path.isdir("backup")!=True:
            os.mkdir("backup")
        c="move "+self.name+" "+("backup\\"+self.name)
        os.system(c)
        #os.remove(self.name)
        self.Close()

    def showALL_FRAME(self,evt):
        for s in ALL_FRAME:
            try:
                s.Show()
            except ImportError:
                ()
    def hideOther_FRAME(self,evt):
        tmp=[]
        tmp+=ALL_FRAME
        tmp.remove(self)
        for s in tmp :   
            try:
                s.Hide()
            except ImportError:
                ()
    def onDeleteAll(self, event):
        global ROOT_DIR
        global ALL_FRAME
        files= os.listdir(ROOT_DIR)
        for s in ALL_FRAME:
            try:
                s.Hide()
                s.Close()
            except ImportError:
                ()
        for m in files:
            if os.path.splitext(m)[1]==".png":
                if os.path.isdir("backup")!=True:
                    os.mkdir("backup")
                    c="move "+ os.path.split(m)[1]+" "+(os.path.split(m)[0]+"\\backup\\" + os.path.split(m)[1])
                    os.system(c)
    def showInExplorer(self, evt):
        os.popen("explorer "+os.getcwd())
    def beWindowsPath(self,cPath):
        newPath=""
        for s in cPath:
            if s=="\\":
                newPath+="/"
            else:
                newPath+=s
        return newPath
    def saveData(self):
        self.miniState=self.IsShown()
        print "save: " ,LANGUAGE_TYPE
        saveChange(MAIN_SETTINGS_TREE,self.name,self.miniState,self.pos,self.scale)
        print "save: " ,SCALE_SPEED
    def showFrameManager(self,event):
        FM=frameManage(parent=None,id=-1)
        FM.Show()
        
                
    def OnKeyDown(self, evt):
        global SCALE_SPEED
        global ADJUST_SCALE_SPEED
        global  ALL_FRAME
        global LANGUAGE_TYPE
        keycode = evt.GetKeyCode()
        ctrldown = evt.ControlDown()
        shiftdown = evt.ShiftDown()
        altdown = evt.AltDown()
        #print (keycode),ctrldown
        #print wx.WXK_CONTROL_V
        '''
        72 H
        67 s
        86 V
        127 delete
        45 -
        61 +
        85 u
         '''
        if 32<=keycode<=126:  
            
            #------------copy and paste image 
            if keycode == 86 and ctrldown and wx.TheClipboard.Open():
                clipBitmap=wx.BitmapDataObject()
                if wx.TheClipboard.GetData(clipBitmap):
                    wx.TheClipboard.Close()    
                    a=random.randint(0, 10000)
                    mapName="ThreeKindom_"+str(a)+"_"+str(int(time.time()))+".png"
                    clipBitmap.GetBitmap().ConvertToImage().SaveFile(mapName,wx.BITMAP_TYPE_PNG)
                    createMap(mapName,True,[(self.pos[0]+7),(self.pos[1]+7)],1)
                    print "paste image from clipboard! "

            if keycode == 67 and ctrldown and os.path.isfile(self.name) and wx.TheClipboard.Open():
                setClipBitmap = wx.BitmapDataObject(wx.Bitmap(self.name, wx.BITMAP_TYPE_PNG))
                wx.TheClipboard.SetData(setClipBitmap)
                wx.TheClipboard.Close()
                print "copy image to clipboard! "
                
                
            #---------scale image 
            if keycode == 45 :
                if ctrldown==False and self.scale>IMAGE_SCALE_MIN_MAX[0]:
                    self.scale=self.scale*(1-SCALE_SPEED)
                    self.resizeMap(self.scale)
                    print "-",self.scale,SCALE_SPEED
                    
                elif   ctrldown and SCALE_SPEED>ADJUST_SCALE_SPEED*2: 
                    SCALE_SPEED-=ADJUST_SCALE_SPEED
                    print SCALE_SPEED
            if keycode == 61 :
                if ctrldown==False and self.scale<IMAGE_SCALE_MIN_MAX[1]:
                    self.scale=self.scale*(SCALE_SPEED+1)
                    self.resizeMap(self.scale)
                    print "+",self.scale,SCALE_SPEED
                
                elif ctrldown and SCALE_SPEED<0.3: 
                    SCALE_SPEED+=ADJUST_SCALE_SPEED
                    print SCALE_SPEED

            #----------hide and show and delete image 
            if keycode==72 and ctrldown:
                if shiftdown:
                    for s in ALL_FRAME:
                        s.Show()
                else:
                    self.Hide()
                
            if keycode == 85 and ctrldown:
                for s in ALL_FRAME:
                    if s.IsShown():
                        s.Hide()
                    else: s.Show()
        if keycode==340:
            #print "help"
            help_Frame= helpFrame(parent=None,id=0)
            help_Frame.Show()
        
        if keycode==127:
            if shiftdown:
                os.remove(self.name)
            else:
                if os.path.isdir("backup")!=True:
                    os.mkdir("backup")
                c="move "+self.name+" "+("backup\\"+self.name)
                os.system(c)
                
            self.Close()
            ALL_FRAME.remove(self)
        if keycode==65 and altdown and ctrldown and shiftdown:
            grapStart(bmp)

#---<string> map path
def createMap(mapPath,state,pos,scale):
    startPos=wx.Point=(pos)
    pos[0]+=SCREEN_POS[0]
    pos[1]+=SCREEN_POS[1]
    tImage=wx.Image(mapPath,wx.BITMAP_TYPE_PNG)
    mapSize=tImage.GetSize()

    newFrame = grapPartFrame(parent=None, id=-1)
    newFrame.pos=pos
    newFrame.miniState=state
    newFrame.scale=scale
    
    newFrame.name=os.path.basename(mapPath)
    newFrame.SetSize(mapSize)
    newFrame.SetPosition(startPos)
    newFrame.bg.SetBitmap(wx.BitmapFromImage(tImage))

    tSize=(newFrame.GetSize()[0]*scale,newFrame.GetSize()[1]*scale)
    tim=tImage.Rescale(newFrame.GetSize()[0]*newFrame.scale,newFrame.GetSize()[1]*scale)
    newFrame.bg.SetBitmap(wx.BitmapFromImage(tim))  
    newFrame.SetWindowShape(wx.BitmapFromImage(tim))
    newFrame.SetSize(tSize)
    saveChange(MAIN_SETTINGS_TREE,newFrame.name,state,pos,scale)
    if state:
        newFrame.Show()
    else:
        newFrame.Hide()
    ALL_FRAME.append(newFrame)

def grap(box):
    global SAVE_SCREEN_MAP_PATH
    global GRAP_PF_NAME
    minSize=40
    if abs(box[2]-box[0])>=minSize and abs(box[3]-box[1])>=minSize:
        gTime=str(int(time.time()))
        save_path=ROOT_DIR+"\\"+GRAP_PF_NAME+"_"+gTime+".png"
        im = Image.open(SAVE_SCREEN_MAP_PATH)
        imSize=()
        cim=Image.new('RGB',(abs(box[2]-box[0]),abs(box[3]-box[1])))
        region = im.crop(box)
        cim.paste(region, (0,0))
        cim.save(save_path)
        createMap(save_path,True,[box[0],box[1]],1)

def screenCapture(savePath,size):
    global SAVE_SCREEN_MAP_PATH
    hwnd = 0  
    hwndDC = win32gui.GetWindowDC(hwnd)   
    mfcDC=win32ui.CreateDCFromHandle(hwndDC)   
    saveDC=mfcDC.CreateCompatibleDC()   
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, size[0], size[1])   
    saveDC.SelectObject(saveBitMap)   
    saveDC.BitBlt((0,0),SCREEN_SIZE, mfcDC, SCREEN_POS, win32con.SRCCOPY)  
    saveBitMap.SaveBitmapFile(saveDC,SAVE_SCREEN_MAP_PATH)  
    Image.open(SAVE_SCREEN_MAP_PATH).save(SAVE_SCREEN_MAP_PATH[:-4]+".png")  

def grapStart(bmp):
    global SCREEN_SIZE
    global SAVE_SCREEN_MAP_PATH
    screenCapture(SAVE_SCREEN_MAP_PATH,SCREEN_SIZE)
    tImage=wx.Image(SAVE_SCREEN_MAP_PATH,wx.BITMAP_TYPE_PNG)
    tImage= tImage.AdjustChannels(1,1,1,0.8)
    mainFrame.bg.SetBitmap(wx.BitmapFromImage(tImage))
    mainFrame.Show()

def start():
    global ROOT_DIR
    global settings_data
    LOG=""
    files= os.listdir(ROOT_DIR)
    i=1
    names=[]
    for m in files:
        nameParts=os.path.basename(m).split("_") 
        if nameParts[0]==GRAP_PF_NAME:
            if os.path.splitext(m)[1]==".png":
                tTree=MAIN_SETTINGS_TREE.find(("images/"+m))
                print MAIN_SETTINGS_TREE.find(("images/"+m)).text
                LOG+="\nname: "+m
                names.append(m)
                try:
                    if tTree.find("miniState").text=="False":
                        miniState=False
                    else:
                        miniState=True
                    pos=[int(tTree.find("posx").text),int(tTree.find("posy").text)]
                    scale=float(tTree.find("scale").text)
                    LOG+="\nload data... : \npos:"+str(pos)+"\nscale: "+str(scale)+"\nminiState: "+str(miniState)
                except:
                    LOG+="can;t get data  miniState pos scale"
                    miniState=False
                    pos=[10,10]
                    scale=1
                    LOG+="\nload fath! set defult data... : \npos:"+str(pos)+"\nscale: "+str(scale)+"\nminiState: "+str(miniState)
                createMap(m,miniState,pos,scale)
                
WMI = GetObject('winmgmts:')
processes = WMI.InstancesOf('Win32_Process')
myCount=0
for s in processes:
    if s.name=="ImagePin.exe":# "python.exe":#
        myCount+=1

if myCount<3:
    # get screen size and pos 
    SCREEN_POS,SCREEN_SIZE=getScreenSizeAndPos()

    #--- get XML settings file Root 
    if  os.path.isfile(SET_FILE_PATH)==False:
        createSetingsFile()
    MAIN_SETTINGS_TREE=ElementTree(file=SET_FILE_PATH).getroot()
    get_settings_data(MAIN_SETTINGS_TREE,settings_data)
    #print "start : ",SCALE_SPEED
    mainApp = wx.PySimpleApp()
    bmp=wx.EmptyBitmap(10,10, depth=-1)
    mainFrame=grapingScreenFrame(parent=None, id=-1)
    mainFrame.bg.SetBitmap(bmp)

    start()
    mainApp.MainLoop()
