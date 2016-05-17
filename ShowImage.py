
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from PIL import Image
import wx,os,time,random
from  xml.etree.ElementTree import*
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
LANGUAGE_PACK=LANGUAGE_PACK_ALL[LANGUAGE_TYPE]
ROOT_DIR=os.getcwd()

ICON_PATH=ROOT_DIR+"/app.ico"
SAVE_SCREEN_MAP_PATH=ROOT_DIR+"/screen.png"
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
    canSize=False
    bSize=SCREEN_SIZE
    sSize=(SCREEN_SIZE[0]*0.1,SCREEN_SIZE[1]*0.1)
    log="ss"
    ID=0
    im=wx.Image(path)
    size=[100,100]
    minSize=[100,50]
    def __init__(self, parent, id,imagePath,im):
        wx.Frame.__init__(self, parent, id, 'fengx', size=SCREEN_SIZE,style=wx.NO_BORDER|wx.STAY_ON_TOP|wx.FRAME_NO_TASKBAR|wx.FRAME_SHAPED)
        tBmp=wx.EmptyBitmap(600,600, depth=-1)
        self.im=im
        self.size=im.GetSize()
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

        maxPix=min(self.size)*self.scale
        minPix=min(self.size)*self.scale

        if (self.scale>1 and  maxPix>IMAGE_MAX_SIZE) or (self.scale<1 and  minPix<IMAGE_MIN_SIZE):
            ()
        elif self.path!="imagePin.png":
            tSize=(self.size[0]*self.scale,self.size[1]*self.scale)
            tim=self.im.Rescale(self.size[0]*self.scale,self.size[1]*self.scale)
            self.bg.SetBitmap(wx.BitmapFromImage(tim))
            self.SetSize(tSize)
            self.SetWindowShape(wx.BitmapFromImage(tim))

    def scaleMap(self,event):
        global SCREEN_SIZE
        if event.GetWheelRotation()<0 and self.path!="imagePin.png" :
            if  self.scale*self.size[0]>IMAGE_MIN_SIZE and self.scale*self.size[1]>IMAGE_MIN_SIZE:
                self.scale=self.scale*(1-SCALE_SPEED)
                self.resizeMap(self.scale)
        elif  self.path!="imagePin.png":
            if  self.scale*self.size[0]< SCREEN_SIZE[0]*1.4 and self.scale*self.size[1]< SCREEN_SIZE[1]*1.4:
                self.scale=self.scale*(1+SCALE_SPEED)
                self.resizeMap(self.scale)

    def OnMouseLeftDclick(self, event):
        if self.path!="imagePin.png":
            newSize=[50,50]
            minSize=60.0
            minScale=1
            mapSize=(self.im.Width,self.im.Height)
            if self.GetSize()[0]<=minSize or self.GetSize()[1]<=minSize:
                tim=self.im.Rescale(self.im.Width,self.im.Height)
                self.bg.SetBitmap(wx.BitmapFromImage(tim))
                self.SetSize((self.im.Width,self.im.Height))
                newPos=[int(self.pos[0]+event.GetPosition()[0]-mapSize[0]/2),int(self.pos[1]+event.GetPosition()[1]-mapSize[1]/2)]
                self.SetPosition(newPos)
                self.pos=newPos
                self.scale=1

            else:
                if self.im.Width>=self.im.Height:
                    minScale=minSize/self.im.Height
                    newSize=(int(self.im.Width*minScale),int(minSize))
                else:
                    minScale=minSize/self.im.Width
                    newSize=(int(minSize),int(self.im.Height*minScale))

                tim=self.im.Rescale(int(self.im.Width*minScale),int(self.im.Height*minScale))
                self.bg.SetBitmap(wx.BitmapFromImage(tim))
                self.SetSize(newSize)
                newPos=[int(self.pos[0]+event.GetPosition()[0]-minSize/2),int(self.pos[1]+event.GetPosition()[1]-minSize/2)]#[int(self.pos[0]+mapSize[0]/2),int(self.pos[1]+mapSize[1]/2)]
                self.SetPosition(newPos)

                self.pos=newPos
                self.scale=minScale
                self.saveData()
            self.SetWindowShape(wx.BitmapFromImage(tim))

    def OnMouseLeftDown(self, event):
        self.lastPos[0]=wx.GetMousePosition()[0]
        self.lastPos[1]=wx.GetMousePosition()[1]
        self.bg.CaptureMouse()

        pos= event.GetPosition()
        box=10
        if self.GetClientSize()[0]-pos[0]<box and self.GetClientSize()[1]-pos[1]<box:
            self.canSize=True
            print "scale:::::;"
            self.canMove=False
        else:
            print "move:::::;"
            self.canSize=False
            self.canMove=True
    def OnMouseLeftUp(self, event):
        self.canMove=False
        self.canSize=False
        if self.bg.HasCapture():
            self.bg.ReleaseMouse()

    def close(self,event):
        if self.path!="imagePin.png":
            self.Close()

    def OnMouseRightDown(self, event):
        print "RightDown"

    def OnMove(self, event):
        #size
        newSizeX=wx.GetMousePosition()[0]-self.lastPos[0]+self.GetClientSize()[0]
        newSizeY=wx.GetMousePosition()[1]-self.lastPos[1]+self.GetClientSize()[1]
        newSize=wx.Point=(newSizeX,newSizeY)
        #move pos
        newPosX=wx.GetMousePosition()[0]-self.lastPos[0]+self.pos[0]
        newPosY=wx.GetMousePosition()[1]-self.lastPos[1]+self.pos[1]
        newPos=wx.Point=(newPosX,newPosY)
        self.mousePos=wx.GetMousePosition()
        if self.canMove and not self.canSize:
            self.SetPosition(newPos)
            self.pos[0]=newPos[0]
            self.pos[1]=newPos[1]
        if not self.canMove and self.canSize :
            #if self.GetClientSize()[1]>self.minSize[1] and self.GetClientSize()[0]>self.minSize[0]:
            self.SetSize(newSize)
        self.lastPos=wx.GetMousePosition()
        box=10
        pos= event.GetPosition()
        #print "size: ",self.GetClientSize()," | pos:",pos
        if self.GetClientSize()[0]-pos[0]<box and self.GetClientSize()[1]-pos[1]<box:
            self.SetCursor(wx.StockCursor(wx.CURSOR_SIZENWSE))
        else:
            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))

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
        bmp=wx.BitmapFromIcon(wx.Icon(os.getcwd()+'/App.ico'))
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
        #imagePinFrame.saveData()
        #for s in ALL_FRAME:
        #    try:
        #        s.saveData()
        #    except:
        #        ()
        #save_settings_data(MAIN_SETTINGS_TREE,settings_data)
        #mainFrame.tbicon.RemoveIcon()
        #self.frame.Close()
        #if os.path.isfile("screen.png"):
        #    os.remove("screen.png")
        #os.system("taskkill /f /im  ImagePin.exe &exit()")
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
        tPath=ROOT_DIR+"/"+self.path
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
        c="move "+self.path+" "+("backup/"+self.path)
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
                    c="move "+ os.path.split(m)[1]+" "+(os.path.split(m)[0]+"/backup/" + os.path.split(m)[1])
                    os.system(c)

    def showInExplorer(self, evt):
        os.popen("explorer "+os.getcwd())

    def beWindowsPath(self,cPath):
        newPath=""
        for s in cPath:
            if s=="/":
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
                    createImage("noname_paste",True,[(self.pos[0]+7),(self.pos[1]+7)],1,mapName)
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
                c="move "+self.path+" "+("backup/"+self.path)
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
                    createImage("noname",True,[int(self.pos[0]*0.33),int(self.pos[1]*0.33)],1,mapName)
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
class PyConsoleFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'fengxEngine', size=(585, 405),style=wx.DEFAULT_FRAME_STYLE)
        #---------------main Window settings----->>>>
        self.SetBackgroundColour((225,225,225))#MAIN_BG_COLOR)
        self.icon = wx.Icon(ICON_PATH, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        import wx.py as py
        self.pyConsole= py.crust.Crust(self)


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
            createImage(name,miniState,pos,scale,path)
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
                    createImage("noname",True,[10,10],1,s)

    imagePin_show=True
    for s in ALL_FRAME:
        if s.IsShown():imagePin_show=False
    if imagePin_show:imagePinFrame.Show()


def createImage(name,state,pos,scale,mapPath):
	startPos=wx.Point=(pos)
	pos[0]+=SCREEN_POS[0]
	pos[1]+=SCREEN_POS[1]
	tImage=wx.Image(mapPath,wx.BITMAP_TYPE_PNG)
	mapSize=tImage.GetSize()

	newFrame = grapPartFrame(parent=None, id=-1,imagePath=mapPath,im=tImage)
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
if __name__ == '__main__':
	mainApp = wx.App()
	print("start")
	bmp=wx.EmptyBitmap(10,10, depth=-1)
	#mainFrame=grapingScreenFrame(parent=None, id=-1)
	#mainFrame.bg.SetBitmap(bmp)

	imagePin_Path="imagePin.png"
	imagePin_Pos=[100,100]
	# imagePinFrame=createImagePinFrame(imagePin_Path,True,imagePin_Pos,1)
	# imagePinFrame=createImagePinFrame(imagePin_Path,True,imagePin_Pos,1)
	# createMap("noname_paste",True,(100,100),1,1,"imagePin")\

	createImage("noname",True,imagePin_Pos,1,imagePin_Path)
	createImage("1",True,[200,200],1,"demo.png")
	#createImage("1",True,[500,500],1,"1.png")
	#testFrame=textFrame(parent=None,id=-1,text="xxxxxxxxxxxxxxx")
	#testFrame.Show()

	#start()
	mainApp.MainLoop()
