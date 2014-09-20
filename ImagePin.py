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
import urllib2
helpInfor_EN='''
    ------------DESCRIPTION---------------------KEYBOARD--------------------MOSUE-----------
    |  grap  image frome screen         |   CTRL+SHIFT+ALT+A     |                         |
    |  copy image to clipboard          |   CTRL    +    C       |                         |
    |  paste image frome clipboard      |   CTRL    +    V       |                         |
    |  delete image                     |   Shift   +    Delete  |                         |
    |  delete image to backup           |   Delete               |                         |
    |  inversion image (show/hide)      |   CTRL    +    U       |                         |
    |  isolation image (show/hide)      |   ALT     +    Q       |                         |
    |                                   |                        |                         |
    |  show in explorer                 |   CTRL     +   D       |                         |
    |  rename image                     |   F2                   |                         |
    |  close image                      |   CTRL    +    W       |                         |
    |  save image                       |   CTRL    +    S       |                         |
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
       单独显示图片 (显示/恢复)             ALT     +    Q                                  

       显示文件位置                         CTRL     +   D                                  
       重命名图片                           F2                                     
       关闭图片                             CTRL    +    W                      
       储存图片                             CTRL    +    S                      
       
       隐藏图片                             CTRL    +    H            鼠标中键单机          
       放大图片                             +                         鼠标滚轮              
       缩小图片                             -                         鼠标滚轮              
       增加(放大/缩小)图片的速度            CTRL    +    +                                  
       减小(放大/缩小)图片的速度            CTRL    +    -                                  
       显示帮助                             F1                                              
                                                                                            
       图片文件拖上已显示的图片快速创建     PNG BMP JPG TGA                                 
    |-----------------------------------|-------------------------|-------------------------|
 '''
EN_Dic = {"grap"              :    "&Grap                -Ctrl+Shift+Alt+A",
    "save"                    :    "&Save as                           -Ctrl+S",
    "help"                    :    "&help                                 -F1",
    "show"                    :    "&Show",
    "hide"                    :    "&Hide                               -Ctr+H",
    "show_all_windows"        :    "Show All Window    -Ctrl+Shift+H",
    "hide_all_windows"        :    "Hide All Window",
    "close"                   :    "&Close                              -Ctrl+C",
    "delete"                  :    "&Delete                             -Delete",
    "exit"                    :    "&Exit",
    "delete_all_images"       :    "Delete All &Images",
    "show_in_explorer"        :    "Show In &Explorer             -Ctrl+D",
    "reset_position"          :    "&Reset Position",
    "hide_others"             :    "Hide &Others                     -Alt+H",
    "help_infor"              :    helpInfor_EN,
    "imagepin_tip"            :    "ImagePin by fengx - zengme@gmail.com",
    "menu_EN"                 :    u"English 英文",
    "menu_CN"                 :    u"Chinese 中文",
    "rename"                  :    u"Rename                               -F2",
    "menu_reName_tip"         :    u"Write a new name: ",
    "menu_reName_tite"        :    u"Rename iamge",
    "menu_reName_pre"         :    u"Name:  "
}

CN_Dic={"grap"                :    "抓取       -Ctrl+Shift+Alt+A",
    "save"                    :    "另存为                  -Ctrl+S",
    "help"                    :    "帮助                        -F1",
    "show"                    :    "显示",
    "hide"                    :    "隐藏                     -Ctr+H",
    "show_all_windows"        :    "显示所有      -Ctrl+Shift+H",
    "hide_all_windows"        :    "隐藏所有",
    "close"                   :    "关闭                     -Ctrl+C",
    "delete"                  :    "删除                     -Delete",
    "exit"                    :    "退出",
    "delete_all_images"       :    "删除所有图片",
    "show_in_explorer"        :    "显示所在文件夹      -Ctrl+D",
    "reset_position"          :    "复位所有图片位置",
    "hide_others"             :    "隐藏其他                -Alt+H",
    "help_infor"              :    helpInfor_CN,
    "imagepin_tip"            :    "ImagePin by fengx - zengme@gmail.com",
    "menu_EN"                 :    u"英文 English",
    "menu_CN"                 :    u"中文 Chinese",
    "rename"                 :    u"重命名                        -F2",
    "menu_reName_tip"         :    u"输入新名字: ",
    "menu_reName_tite"        :    u"重命名图片",
    "menu_reName_pre"         :    u"名字:  "
}

LANGUAGE_TYPE=0

LANGUAGE_PACK_ALL=[EN_Dic,CN_Dic]
#LANGUAGE_PACK=LANGUAGE_PACK_ALL[LANGUAGE_TYPE]
ROOT_DIR=os.getcwd()

ICON_PATH=ROOT_DIR+"\\app.ico"
SAVE_SCREEN_MAP_PATH=ROOT_DIR+"\\screen.png"
SET_FILE_PATH="sttings.fengx"
GRAP_PF_NAME="fengx"

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

TEST_FRAME=[]

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
    print "\nscrenRect: ",screenPS
    return screenPS

#  -------------- xmlz
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
    print files
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
    print "\nsaveChange: ",name
def save_settings_data(mainTree,data):
    for s in data:
        if mainTree.find(s)!=None:
            if s=="ICON_PATH" or s=="SAVE_SCREEN_MAP_PATH" or s=="SET_FILE_PATH" or s=="GRAP_PF_NAME"  or s=="GRAP_PF_NAME" :
                mainTree.find(s).text=str(data[s])
            else:
                mainTree.find(s).text=str(data[s])#str(data[s])

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

SCREEN_POS,SCREEN_SIZE=getScreenSizeAndPos()
#--- get XML settings file Root 
if  os.path.isfile(SET_FILE_PATH)==False:
    createSetingsFile()
MAIN_SETTINGS_TREE=ElementTree(file=SET_FILE_PATH).getroot()
get_settings_data(MAIN_SETTINGS_TREE,settings_data)

LANGUAGE_PACK=LANGUAGE_PACK_ALL[settings_data["LANGUAGE_TYPE"]]

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
            importOn=False
            for s in file_types:
                
                if fileE==s:
                    i+=1
                    im = Image.open(f)
                    mapName=GRAP_PF_NAME+"_"+str(i)+"_"+str(int(time.time()))+".png"
                    im.save(mapName,format="png")
                    print "import  image  succeed: " ,f
                    importOn=True
                    createMap("noname",True,[int(self.pos[0]*0.33),int(self.pos[1]*0.33)],1,mapName)
            if importOn==False: print "import image  failure: ",f
            

class MyURLDropTarget(wx.PyDropTarget):
    def __init__(self, window):
        wx.PyDropTarget.__init__(self)
        self.window = window

        self.data = wx.URLDataObject();
        self.SetDataObject(self.data)

    def OnDragOver(self, x, y, d):
        return wx.DragLink

    def OnData(self, x, y, d):
        if not self.GetData():
            return wx.DragNone

        url = self.data.GetURL()
        self.window.AppendText(url + "\n")

        return d
class helpFrame(wx.Frame):
    global LANGUAGE_TYPE,MAIN_SETTINGS_TREE ,settings_data
    def __init__(self, parent,id):
        global LANGUAGE_TYPE
        helpSize=(900,420)
        windowSize=(helpSize[0],(helpSize[1]+120))
        wx.Frame.__init__(self, parent, id, 'ImagePin_help', size=windowSize,style=wx.DEFAULT_FRAME_STYLE)
        self.SetBackgroundColour((67,67,67))
        self.main_P=wx.Panel(self)
        help_text=wx.StaticText(self.main_P, -1, LANGUAGE_PACK["help_infor"])#, pos=(0,0),size=helpSize)
        font = wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL)
        help_text.SetFont(font)
        help_text.SetForegroundColour((29,29,29))
        help_text.SetBackgroundColour((75,75,75))
  
        fengx_text=wx.StaticText(self.main_P, -1, LANGUAGE_PACK["imagepin_tip"])#, pos=(0,0),size=helpSize)
        fengx_text.SetForegroundColour((45,45,45))
        box1_title = wx.StaticBox( self.main_P, -1, " " )
        box1 = wx.StaticBoxSizer( box1_title, wx.VERTICAL, )
        
        box1.Add( help_text, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
        box1.Add( fengx_text, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
        self.main_P.SetSizer(box1)
        box1.Fit( self.main_P )
        
# tabbar icon class
class TB_Icon(wx.TaskBarIcon):
    global ICON_PATH
    global ALL_FRAME
    global settings_data
    global LANGUAGE_TYPE
    global MAIN_SETTINGS_TREE
    global imagePinFrame
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
    m_EN=wx.NewId()
    m_CN=wx.NewId()
    
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon( wx.Icon(ICON_PATH, wx.BITMAP_TYPE_ICO), LANGUAGE_PACK["imagepin_tip"])
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
        self.Bind(wx.EVT_MENU, self.changeToEN,id=self.m_EN)
        self.Bind(wx.EVT_MENU, self.changeToCN,id=self.m_CN)
        
    

    
    def CreatePopupMenu(self):
    
        
        menu= wx.Menu()
        menu.AppendSeparator()
        #menu.Append(self.m_frameManager,"FrameManager")
        menu.Append(self.m_screenGrap, LANGUAGE_PACK["grap"])
        menu.Append(self.m_show, LANGUAGE_PACK["show_all_windows"]) 
        menu.Append(self.m_hide,  LANGUAGE_PACK["hide_all_windows"])
        menu.Append(self.m_showInExplorer, LANGUAGE_PACK["show_in_explorer"])
        menu.AppendSeparator()
        menu.Append(self.m_EN, LANGUAGE_PACK["menu_CN"])
        menu.Append(self.m_CN, LANGUAGE_PACK["menu_EN"])
        menu.Append(self.m_help,LANGUAGE_PACK["help"])
        menu.AppendSeparator()
        menu.Append(self.m_reset,LANGUAGE_PACK["reset_position"])
        menu.Append(self.m_DeleteAll, LANGUAGE_PACK["delete_all_images"])
        menu.Append(self.m_close, LANGUAGE_PACK["exit"])
        
        
        return menu


    def OnTaskBarActivate(self, evt):
        imagePinFrame.Show()
        #grapStart(bmp)
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

    def changeToEN(self,evt):
        LANGUAGE_TYPE=0
        save_settings_data(MAIN_SETTINGS_TREE,settings_data)
    def changeToCN(self,evt):
        LANGUAGE_TYPE=1
        save_settings_data(MAIN_SETTINGS_TREE,settings_data)


        
    def reset(self,evt):
        i=0
        for s in ALL_FRAME:
            i+=1
            try:
                s.show()
                s.hide=False
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
                s.hide=False
            except ImportError:
                ()
                
    def hideALL_FRAME(self,evt):
        for s in ALL_FRAME:   
            try:
                s.Hide()
                s.hide=True
            except ImportError:
                ()
    
    def closeApp(self, evt):
        imagePinFrame.saveData()
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
    #global LANGUAGE_TYPE
    global TEST_FRAME
    global imagePinFrame
    global mainFrame
    name="no name"
    path="imagePin.png"
    isolation=False
    miniState=False
    hide=False
    pos=SCREEN_POS
    mousePos=[0,0]
    scale=1
    lastPos=[0,0]
    canMove=False
    bSize=SCREEN_SIZE
    sSize=(SCREEN_SIZE[0]*0.1,SCREEN_SIZE[1]*0.1)
    log="ss"
    ID=0
    
    def __init__(self, parent, id,imagePath):
        wx.Frame.__init__(self, parent, id, 'fengx', size=SCREEN_SIZE,style=wx.NO_BORDER|wx.STAY_ON_TOP|wx.FRAME_NO_TASKBAR|wx.FRAME_SHAPED)
        tBmp=wx.EmptyBitmap(600,600, depth=-1)
        self.bg=wx.StaticBitmap(self,-1,  tBmp, (0,0))
        self.bg.Bind(wx.EVT_MOTION,  self.OnMove)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        self.Bind(wx.EVT_KEY_DOWN,self.OnKeyDown)
        self.bg.SetDropTarget( MyFileDropTarget(self.bg,SCREEN_SIZE) ) 
        
        self.bg.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.bg.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        


        self.bg.Bind(wx.EVT_LEFT_DCLICK, self.OnMouseLeftDclick)
        self.bg.Bind(wx.EVT_MIDDLE_UP,  self.onHide)
        self.Bind(wx.EVT_MOUSEWHEEL, self.scaleMap)
        self.path=imagePath
        
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
        im=wx.Image(self.path)
        size=im.GetSize()
        maxPix=min(size)*self.scale
        minPix=min(size)*self.scale
        
        if (self.scale>1 and  maxPix>IMAGE_MAX_SIZE) or (self.scale<1 and  minPix<IMAGE_MIN_SIZE):
            ()
        elif self.path!="imagePin.png":
            tSize=(size[0]*self.scale,size[1]*self.scale)
            tim=im.Rescale(size[0]*self.scale,size[1]*self.scale)
            self.bg.SetBitmap(wx.BitmapFromImage(tim))  
            self.SetSize(tSize)  
            self.SetWindowShape(wx.BitmapFromImage(tim))

    def scaleMap(self,event):
        global SCREEN_SIZE
        im=wx.Image(self.path)
        size=im.GetSize()
        if event.GetWheelRotation()<0 and self.path!="imagePin.png" :
            if  self.scale*size[0]>IMAGE_MIN_SIZE and self.scale*size[1]>IMAGE_MIN_SIZE:
                self.scale=self.scale*(1-SCALE_SPEED)
                self.resizeMap(self.scale)
        elif  self.path!="imagePin.png": 
            if  self.scale*size[0]< SCREEN_SIZE[0]*1.4 and self.scale*size[1]< SCREEN_SIZE[1]*1.4:
                self.scale=self.scale*(1+SCALE_SPEED)
                self.resizeMap(self.scale)

    def OnMouseLeftDclick(self, event):  
        if self.path!="imagePin.png":
            im=wx.Image(self.path) 
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
            self.SetWindowShape(wx.BitmapFromImage(tim))

    def OnMouseLeftDown(self, event):
        self.lastPos[0]=event.GetPosition()[0]
        self.lastPos[1]=event.GetPosition()[1]
        self.canMove=True
        self.bg.CaptureMouse()

    def OnMouseLeftUp(self, event):
        self.canMove=False
        if self.bg.HasCapture():
            self.bg.ReleaseMouse()
    def close(self,event):
        if self.path!="imagePin.png":
            self.Close()

    def OnMouseRightDown(self, event):
        print "RightDown"

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
            
            self.pp_test=wx.NewId()
            self.pp_RENAME=wx.NewId()
            self.pp_EXIT=wx.NewId()
            self.Bind(wx.EVT_MENU, self.onSave, id=self.pp_SAVE)
            self.Bind(wx.EVT_MENU, self.onClose, id=self.pp_CLOSE)
            self.Bind(wx.EVT_MENU, self.onDelete, id=self.pp_DELETE)    

            self.Bind(wx.EVT_MENU, self.showALL_FRAME, id=self.pp_SHOW_ALL)
            self.Bind(wx.EVT_MENU, self.hideOther_FRAME, id=self.pp_HIDE_OTHER)
            self.Bind(wx.EVT_MENU, self.onHide, id=self.pp_HIDE)
            self.Bind(wx.EVT_MENU, self.grapScreen, id=self.pp_GRAP)
            self.Bind(wx.EVT_MENU, self.showFrameManager, id=self.pp_FRAMEMANAGER)
            self.Bind(wx.EVT_MENU, self.showInExplorer, id=self.pp_SHOWINEXPLORER)
            self.Bind(wx.EVT_MENU, self.reName, id=self.pp_RENAME)
            self.Bind(wx.EVT_MENU,self.closeApp,id=self.pp_EXIT)
        bmp=wx.BitmapFromIcon(wx.Icon(os.getcwd()+'\\App.ico'))
        menu = wx.Menu()
        if self.path!="imagePin.png":
            menu.Append(self.pp_RENAME, (LANGUAGE_PACK["menu_reName_pre"]+self.name))
            menu.AppendSeparator()
        # menu.Append(self.pp_test, self.name)
            menu.Append(self.pp_RENAME, (LANGUAGE_PACK["rename"]))#+"--- "+self.name))
        menu.AppendSeparator()
        menu.Append(self.pp_GRAP,LANGUAGE_PACK["grap"])
        menu.Append(self.pp_SHOWINEXPLORER, LANGUAGE_PACK["show_in_explorer"])
        menu.Append(self.pp_HIDE, LANGUAGE_PACK["hide"])
        menu.Append(self.pp_HIDE_OTHER, LANGUAGE_PACK["hide_others"])
        menu.Append(self.pp_SHOW_ALL, LANGUAGE_PACK["show_all_windows"])
        if self.path!="imagePin.png":
            menu.AppendSeparator()
            item = wx.MenuItem(menu, self.pp_SAVE,LANGUAGE_PACK["save"])
            menu.AppendItem(item)
            menu.Append(self.pp_CLOSE, LANGUAGE_PACK["close"])
            menu.Append(self.pp_DELETE, LANGUAGE_PACK["delete"])
        menu.Append(self.pp_EXIT,LANGUAGE_PACK["exit"])
        self.PopupMenu(menu)
        menu.Destroy()
 
    def closeApp(self,event):
        imagePinFrame.saveData()
        for s in ALL_FRAME:
            try:
                s.saveData()
            except:
                ()
        save_settings_data(MAIN_SETTINGS_TREE,settings_data)
        mainFrame.tbicon.RemoveIcon()
        #self.frame.Close()
        if os.path.isfile("screen.png"):
            os.remove("screen.png")
        os.system("taskkill /f /im  ImagePin.exe &exit()")
        sys.exit()
        
    def reName(self, evt):
        dlg = wx.TextEntryDialog(
                self, LANGUAGE_PACK["menu_reName_tip"],
                LANGUAGE_PACK["menu_reName_tite"], "imagePin")
        dlg.SetValue(self.name)

        if dlg.ShowModal() == wx.ID_OK:
            print "rename : ",self.name,"to : ",dlg.GetValue()
            self.name=dlg.GetValue()
        dlg.Destroy()

    def grapScreen(self, evt):
        grapStart(bmp)

    def onSave(self,event):
        wildcard = "png (*.png)|*.png|bmp (*.bmp)|*.bmp|tga (*.tga)|*.tga|jpg (*.jpg)|*.jpg|"     \
        "All files (*.*)|*.*"
        dialog=wx.FileDialog(self, message="Save file as ...", defaultDir=os.getcwd(), 
        
         defaultFile=self.name, wildcard=wildcard,style=wx.SAVE)
        
        tPath=os.path.dirname(self.path) 
        tPath=ROOT_DIR+"\\"+self.path
        if dialog.ShowModal()==wx.ID_OK:
            im = Image.open(self.path)
            #file_et=os.path.splitext(dialog.GetPath())[1]
            im.save(dialog.GetPath())#,format=file_et)
            print "save ",self.name," to  : ",dialog.GetPath()
        dialog.Destroy()

    def onClose(self, event):
        ALL_FRAME.remove(self)
        self.saveData()
        self.Close()

    def onHide(self, event):
        self.miniState=False
        self.saveData()
        self.Hide()
        self.hide=True

    def onDelete(self, event):
        global  ALL_FRAME
        ALL_FRAME.remove(self)
        if os.path.isdir("backup")!=True:
            os.mkdir("backup")
        c="move "+self.path+" "+("backup\\"+self.path)
        os.system(c)
        #os.remove(self.path)
        self.Close()

    def showALL_FRAME(self,evt):
        for s in ALL_FRAME:   
            if s !=self:
                s.Show()
                s.hide=False

    def hideOther_FRAME(self,evt):
        for s in ALL_FRAME:   
            if s !=self:
                s.Hide()
                s.hide=True
            
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
        saveChange(MAIN_SETTINGS_TREE,self.name,self.miniState,self.pos,self.scale,self.path)
        
    def showFrameManager(self,event):
        FM=frameManage(parent=None,id=-1)
        FM.Show()
 
    def OnKeyDown(self, evt):
        global SCALE_SPEED
        global ADJUST_SCALE_SPEED
        global  ALL_FRAME
        global LANGUAGE_TYPE
        tempFrame=[]
        
        keycode = evt.GetKeyCode()
        ctrldown = evt.ControlDown()
        shiftdown = evt.ShiftDown()
        altdown = evt.AltDown()
        #print (keycode)
        #,ctrldown
        #print wx.WXK_CONTROL_V
        '''
        72 H
        67 s
        86 V
        127 delete
        45 -
        61 +
        85 u
        341    F2
        83     S
        68     D
        67     C
         '''
        if 32<=keycode<=126:  
            
            #------------copy and paste image 
            if keycode == 86 and ctrldown and wx.TheClipboard.Open():
                clipBitmap=wx.BitmapDataObject()
                if wx.TheClipboard.GetData(clipBitmap):
                    wx.TheClipboard.Close()    
                    a=random.randint(0, 10000)
                    mapName=GRAP_PF_NAME+"_"+str(a)+"_"+str(int(time.time()))+".png"
                    clipBitmap.GetBitmap().ConvertToImage().SaveFile(mapName,wx.BITMAP_TYPE_PNG)
                    createMap("noname_paste",True,[(self.pos[0]+7),(self.pos[1]+7)],1,mapName)
                    print "paste image from clipboard! "
            if keycode == 67 and ctrldown and os.path.isfile(self.path) and wx.TheClipboard.Open() and self.path!="imagePin.png":
                setClipBitmap = wx.BitmapDataObject(wx.Bitmap(self.path, wx.BITMAP_TYPE_PNG))
                wx.TheClipboard.SetData(setClipBitmap)
                wx.TheClipboard.Close()
                print "copy image to clipboard! "
                
                
            #---------scale image 
            if keycode == 45 :
                if ctrldown==False and self.scale>IMAGE_SCALE_MIN_MAX[0] and self.path!="imagePin.png":
                    self.scale=self.scale*(1-SCALE_SPEED)
                    self.resizeMap(self.scale)
                    print "-",self.scale,SCALE_SPEED
                    
                elif   ctrldown and SCALE_SPEED>ADJUST_SCALE_SPEED*2: 
                    SCALE_SPEED-=ADJUST_SCALE_SPEED
                    print "SCALE_SPEED",SCALE_SPEED
            if keycode == 61 :
                if ctrldown==False and self.scale<IMAGE_SCALE_MIN_MAX[1]and self.path!="imagePin.png":
                    self.scale=self.scale*(SCALE_SPEED+1)
                    self.resizeMap(self.scale)
                    print "+",self.scale,SCALE_SPEED
                
                elif ctrldown and SCALE_SPEED<0.3: 
                    SCALE_SPEED+=ADJUST_SCALE_SPEED
                    print "SCALE_SPEED",SCALE_SPEED

            #----------hide and show and delete image 
            if keycode==72 and ctrldown and self.path!="imagePin.png":
                if shiftdown:
                    for s in ALL_FRAME:
                        s.Show()
                        s.hide=False
                else:
                    self.Hide()
                    s.hide=True
                
            if keycode == 85 and ctrldown:
                temp=True
                for s in ALL_FRAME:
                    if s.IsShown():
                        s.Hide()
                        s.hide=True
                    else:
                        s.Show()
                        s.hide=False
                        
                    if s.IsShown():temp=False
                if temp: imagePinFrame.Show() 
                else: imagePinFrame.Hide()
            if keycode == 81 and altdown: 
                if self.isolation:
                    for s in ALL_FRAME:   
                        if s !=self and s.hide==False:
                            s.Show()
                    self.isolation=False            
                else:
                    for s in ALL_FRAME:   
                        if s !=self and s.hide==False:
                            s.Hide()
                    self.isolation=True
            #-----------save         
            if keycode == 83 and ctrldown:
                self.onSave(evt)
            #----------showInExplorer
            if keycode == 68 and ctrldown:
                self.showInExplorer(evt)            
            #----------showInExplorer
            if keycode == 87 and ctrldown:
                self.onClose(evt)
                
        if keycode==342:
            if ctrldown and shiftdown and altdown:
                console=PyConsoleFrame(parent=None,id=-1)
                console.Show()                
        if keycode==341:
            self.reName(evt)
            if ctrldown and shiftdown and altdown:        
                console=pyConsole(parent=None,id=-1,text="xxxxxxxxxxxxxxx")
                console.Show()
        if keycode==340:
            #print "help"
            help_Frame= helpFrame(parent=None,id=0)
            help_Frame.Show()
        
        if keycode==127 and self.path!="imagePin.png":
            if shiftdown:
                os.remove(self.path)
            else:
                if os.path.isdir("backup")!=True:
                    os.mkdir("backup")
                c="move "+self.path+" "+("backup\\"+self.path)
                os.system(c)
                
            self.Close()
            ALL_FRAME.remove(self)
        if keycode==65 and altdown and ctrldown and shiftdown:
            grapStart(bmp)


class textFrame(wx.Frame):
    BG_COLOR=(67,67,67)
    FG_COLOR=(120,120,120)
    SIZE=(242 ,256)
    lastPos=[0,0]
    canMove=False
    canSize=False
    mousePos=[0,0]
    pos=[400,300]
    size=[0,0]
    
    
    def __init__( self, parent,id,text ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "fengx", pos = wx.DefaultPosition, size = wx.Size( 342,335 ), style = wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.Size( 100,170 ), wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
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
    
    
    
    
    
    
    
    
    
    
    
    
    # def __init__(self, parent, id,text):
        # wx.Frame.__init__(self, parent, id, 'fengxEngine',pos=(self.pos[0],self.pos[1]),size=self.SIZE,style=wx.NO_BORDER|wx.STAY_ON_TOP|wx.FRAME_NO_TASKBAR|wx.FRAME_SHAPED)
        # self.SetBackgroundColour(self.BG_COLOR)
        # self.text=text        
        
        # self.main_P=wx.Panel(self,size=self.SIZE)
       # self.main_P.SetBackgroundColour(self.BG_COLOR)
        # self.sizebar=wx.Panel(self.main_P,pos=(0,self.SIZE[1]-12),size=(2000,2000))
        # #self.sizebar=wx.Panel(self.main_P,pos=(0,self.SIZE[1]-12),size=(self.SIZE[0],self.SIZE[1]))
        self.sizebar.SetBackgroundColour((63,63,63))
        # self.textC= wx.TextCtrl(self.main_P,-1, self.text,pos=(-2,26),size=((self.SIZE[1]+6),self.SIZE[1]-35), style=wx.TE_MULTILINE|wx.TE_RICH2)
        font = wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,False,"微软雅黑")#"Micrisoft YaHei")
        self.textC.SetFont(font)
        self.textC.SetBackgroundColour(self.BG_COLOR)
        self.textC.SetForegroundColour(self.FG_COLOR)
        
        # self.movebar=wx.Panel(self.main_P,pos=(0,0),size=(self.SIZE[0],30))
        self.movebar.SetBackgroundColour((59,59,59))
        
        
        # b_add_bmp = wx.Bitmap("text_b_add.bmp", wx.BITMAP_TYPE_BMP)
        # b_close_bmp = wx.Bitmap("text_b_close.bmp", wx.BITMAP_TYPE_BMP)
        # b_add_mask= wx.Mask(b_add_bmp, wx.BLUE)
        # b_close_mask= wx.Mask(b_close_bmp, wx.BLUE)
        # b_add_bmp.SetMask(b_add_mask)
        # b_close_bmp.SetMask(b_add_mask)

        #self.b_add=wx.BitmapButton(self.movebar, -1, b_add_bmp, (5,5),(20, 20),style = wx.NO_BORDER)
        # self.b_add.SetBackgroundColour((19,120,20))
 
        #self.b_close=wx.BitmapButton(self.movebar,-1,"xx",size=(20,20),pos=((self.SIZE[0]-25),5))
        # self.b_close.SetBackgroundColour((19,120,20))


        
        self.movebar.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp) 
        self.movebar.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown) 
        self.movebar.Bind(wx.EVT_MOTION,  self.OnMove)
        
        self.sizebar.Bind(wx.EVT_LEFT_UP, self.OnSizeMouseLeftUp) 
        self.sizebar.Bind(wx.EVT_LEFT_DOWN, self.OnSizeMouseLeftDown) 
        self.sizebar.Bind(wx.EVT_MOTION,  self.OnSizeMove)
        # self.textC.Bind(wx.EVT_MOTION, self.OnStartDrag)
        # self.textC.SetDropTarget(MyURLDropTarget(self.textC))  
   
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
        newSizeX=event.GetPosition()[0]-self.lastPos[0]+self.GetClientSize()[0]
        newSizeY=event.GetPosition()[1]-self.lastPos[1]+self.GetClientSize()[1]
        newSize=wx.Point=(newSizeX,newSizeY)
        print "self.lastPos",self.lastPos
        print event.GetPosition()[0]-self.lastPos[0],event.GetPosition()[1]-self.lastPos[1]
        print "event.GetPosition()",event.GetPosition()
        print "self.GetClientSize()",self.GetClientSize()
        if self.canSize:
            self.SetSize(newSize) 
        self.lastPos[0]=event.GetPosition()[0]
        self.lastPos[1]=event.GetPosition()[1]
        
    def OnSizeMouseLeftDown(self, event):
        self.sizebar.CaptureMouse()
        self.lastPos[0]=event.GetPosition()[0]
        self.lastPos[1]=event.GetPosition()[1]
        self.canSize=True


    def OnSizeMouseLeftUp(self, event):
        if self.sizebar.HasCapture():
            self.sizebar.ReleaseMouse()          
        self.canSize=False
    def OnClick(self, event):
        self.log.write("Click! (%d)\n" % event.GetId())


        
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

    def OnMouseLeftDown(self, event):
        self.movebar.CaptureMouse()
        self.lastPos[0]=event.GetPosition()[0]
        self.lastPos[1]=event.GetPosition()[1]
        self.canMove=True
    
    def OnMouseLeftUp(self, event):
        if self.movebar.HasCapture():
            self.movebar.ReleaseMouse()          
        self.canMove=False
class PyConsoleFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'fengxEngine', size=(585, 405),style=wx.DEFAULT_FRAME_STYLE)
        #---------------main Window settings----->>>>
        self.SetBackgroundColour((225,225,225))#MAIN_BG_COLOR)
        self.icon = wx.Icon(ICON_PATH, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        import wx.py as py
        self.pyConsole= py.crust.Crust(self)
        
        
def createMap(name,state,pos,scale,mapPath):
    startPos=wx.Point=(pos)
    pos[0]+=SCREEN_POS[0]
    pos[1]+=SCREEN_POS[1]
    tImage=wx.Image(mapPath,wx.BITMAP_TYPE_PNG)
    mapSize=tImage.GetSize()

    newFrame = grapPartFrame(parent=None, id=-1,imagePath=mapPath)
    newFrame.pos=pos
    newFrame.miniState=state
    newFrame.scale=scale
    
    #set toolTip
    newFrame.bg.ToolTip=wx.ToolTip(name)
    newFrame.bg.ToolTip.SetDelay(long(2900)) 
    
    newFrame.name=name
    newFrame.SetSize(mapSize)
    newFrame.SetPosition(startPos)
    newFrame.bg.SetBitmap(wx.BitmapFromImage(tImage))

    tSize=(newFrame.GetSize()[0]*scale,newFrame.GetSize()[1]*scale)
    tim=tImage.Rescale(newFrame.GetSize()[0]*newFrame.scale,newFrame.GetSize()[1]*scale)
    newFrame.bg.SetBitmap(wx.BitmapFromImage(tim))  
    newFrame.SetWindowShape(wx.BitmapFromImage(tim))
    newFrame.SetSize(tSize)
    #saveChange(MAIN_SETTINGS_TREE,newFrame.name,state,pos,scale,mapPath)
    if state:
        newFrame.Show()
    else:
        newFrame.Hide()
    ALL_FRAME.append(newFrame)
    print "\ncreateMap: " , "\n    name: ",name,"\n    path: ",mapPath

def createImagePinFrame(mapPath,state,pos,scale):
    startPos=wx.Point=(pos)
    pos[0]+=SCREEN_POS[0]
    pos[1]+=SCREEN_POS[1]
    tImage=wx.Image(mapPath,wx.BITMAP_TYPE_PNG)
    mapSize=tImage.GetSize()

    newFrame = grapPartFrame(parent=None, id=-1,imagePath=mapPath)
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

    return newFrame
    
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
        createMap(os.path.basename(save_path).replace(".png",""),True,[box[0],box[1]],1,save_path)

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
    print "grapStart: "
    
def start():
    global ROOT_DIR
    global settings_data
    LOG=""
    files= os.listdir(ROOT_DIR)

    
    loadedImages=[]
    imagesDate=MAIN_SETTINGS_TREE.findall("images/image")
    
    for s in imagesDate:
        #print s.find("name").text
        #print s.find("miniState")
        miniState=True
        if s.find("miniState").text=="False":
            miniState=False
        else:
            miniState=True
        pos=[int(s.find("posx").text),int(s.find("posy").text)]
        scale=float(s.find("scale").text)
        path=s.find("path").text
        name=s.find("name").text
        if os.path.isfile(path):
            createMap(name,miniState,pos,scale,path)
            loadedImages.append(path)
            
        else:
            print "\nremove exist  file setting's data: " ,"\n   name: ",s.find("name").text,"\n   path: ",s.find("path").text
            s.find("path").text="delete"
            imagesDate.remove(s)
            MAIN_SETTINGS_TREE.findall("images/image").remove(s)

    for s in files:
        nameParts=os.path.basename(s).split("_") 
        if nameParts[0]==GRAP_PF_NAME:
            if os.path.splitext(s)[1]==".png":
                if s not in loadedImages:
                    createMap("noname",True,[10,10],1,s) 
            
            
    
    
    # for m in files:
        # nameParts=os.path.basename(m).split("_") 
        # if nameParts[0]==GRAP_PF_NAME:
            # if os.path.splitext(m)[1]==".png":
                # tTree=MAIN_SETTINGS_TREE.find(("images/"+m))
                # #print MAIN_SETTINGS_TREE.find(("images/"+m)).text
                # LOG+="\nname: "+m
                # names.append(m)
                
                # try:
                    # if tTree.find("miniState").text=="False":
                    # else:
                        # miniState=True
                    # pos=[int(tTree.find("posx").text),int(tTree.find("posy").text)]
                    # scale=float(tTree.find("scale").text)
                    # path=float(tTree.find("path").text)
                    
                    # LOG+="\nload data... : \npos:"+str(pos)+"\nscale: "+str(scale)+"\nminiState: "+str(miniState)
                # except:
                    # LOG+="can;t get data  miniState pos scale"
                    # miniState=False
                    # pos=[10,10]
                    # scale=1
                    # path=m
                    # LOG+="\nload fath! set defult data... : \npos:"+str(pos)+"\nscale: "+str(scale)+"\nminiState: "+str(miniState)
                # createMap(m,miniState,pos,scale,path)

        
    imagePin_show=True
    for s in ALL_FRAME:
        if s.IsShown():imagePin_show=False
    if imagePin_show:imagePinFrame.Show()



if __name__ == '__main__':
        
    WMI = GetObject('winmgmts:')
    processes = WMI.InstancesOf('Win32_Process')
    myCount=0
    for s in processes:
        if s.name=="ImagePin.exe":# "python.exe":#
            myCount+=1

            
    if myCount<3:
        # get screen size and pos 

        
        #print "start : ",SCALE_SPEED
        mainApp = wx.App()
        bmp=wx.EmptyBitmap(10,10, depth=-1)
        mainFrame=grapingScreenFrame(parent=None, id=-1)
        mainFrame.bg.SetBitmap(bmp)
        
        imagePin_Path="imagePin.png"   
        imagePin_Pos=[100,100]
        imagePinFrame=createImagePinFrame(imagePin_Path,True,imagePin_Pos,1)
        
        #testFrame=textFrame(parent=None,id=-1,text="xxxxxxxxxxxxxxx")
        #testFrame.Show()

        start()
        mainApp.MainLoop()