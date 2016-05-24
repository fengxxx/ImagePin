
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from PIL import Image
import wx,os,time,random,pyautogui
from  xml.etree.ElementTree import*
from _globalData import *
from _imagePinUtil import *

class grapPartFrame(wx.Frame):
    global SCREEN_SIZE
    global SCREEN_POS
    global SCALE_SPEED
    global ADJUST_SCALE_SPEED
    global IMAGE_MAX_SIZE
    global IMAGE_MIN_SIZE
    global MAIN_SETTINGS_TREE
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
    scale=1
    lastPos=[0,0]
    lastPosSize=[0,0]
    canMove=False
    canSize=False
    bSize=SCREEN_SIZE
    sSize=(SCREEN_SIZE[0]*0.1,SCREEN_SIZE[1]*0.1)
    log="ss"
    ID=0
    im=wx.Image(path)
    im_sizenwse=wx.Image("CURSOR_SIZENWSE.png")
    im_sizenwse.SetMaskColour(0,0,255)
    #im_sizenwse.SetMaskColour(0,0,255)
    size=[100,100]
    minSize=[100,50]
    sizeSize=[32,32]
    def __init__(self, parent, id,imagePath,im):
        wx.Frame.__init__(self, parent, id, 'fengx', size=SCREEN_SIZE,style=wx.NO_BORDER|wx.STAY_ON_TOP|wx.FRAME_NO_TASKBAR|wx.FRAME_SHAPED)
        tBmp=wx.EmptyBitmap(600,600, depth=-1)
        self.im=im
        self.size=im.GetSize()
        self.bg=wx.StaticBitmap(self,-1,  tBmp, (0,0))
        #self.b_sizenwse=wx.StaticBitmap(self.bg,-1,  tBmp, (-self.im_sizenwse.Width,-self.im_sizenwse.Height))
        self.b_sizenwse=wx.BitmapButton(self.bg,-1,  tBmp, (-self.im_sizenwse.Width,-self.im_sizenwse.Height),size=(self.im_sizenwse.Width,self.im_sizenwse.Height))
        #bmp = wx.Bitmap("CURSOR_SIZENWSE.png", wx.BITMAP_TYPE_ANY)
        #button = wx.BitmapButton(self.bg, id=wx.ID_ANY, bitmap=bmp, size=(bmp.GetWidth()+10, bmp.GetHeight()+10))
        #button.SetPosition((10,10))
        self.b_sizenwse.SetBitmap(wx.BitmapFromImage(self.im_sizenwse))
        self.b_sizenwse.Bind(wx.EVT_LEFT_DOWN,self.OnMouseLeftDown_size)
        self.b_sizenwse.Bind(wx.EVT_LEFT_UP,self.OnMouseLeftUp_size)
        self.b_sizenwse.Bind(wx.EVT_MOTION,  self.OnMoveSize)
        self.bg.Bind(wx.EVT_MOTION,  self.OnMove)
        self.bg.SetDropTarget( MyFileDropTarget(self.bg,SCREEN_SIZE) )
        self.bg.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.bg.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.bg.Bind(wx.EVT_LEFT_DCLICK, self.OnMouseLeftDclick)
        self.bg.Bind(wx.EVT_MIDDLE_UP,  self.onHide)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        self.Bind(wx.EVT_KEY_DOWN,self.OnKeyDown)
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
            #bbmp.SetMaskColour(wx.BLUE)
            self.dc.DrawBitmap(bbmp, 0,0, True)

    def resizeMap(self,sc):
        maxPix=min(self.size)*self.scale
        minPix=min(self.size)*self.scale
        if (self.scale>1 and  maxPix>IMAGE_MAX_SIZE) or (self.scale<1 and  minPix<IMAGE_MIN_SIZE):
            ()
        elif self.path!="imagePin.png":
            tSize=(self.size[0]*self.scale,self.size[1]*self.scale)
            tim=self.im.Copy().Rescale(self.size[0]*self.scale,self.size[1]*self.scale)
            self.bg.SetBitmap(wx.BitmapFromImage(tim))
            self.SetSize(tSize)
            self.SetWindowShape(wx.BitmapFromImage(tim))
        #self.b_sizenwse.SetPosition((self.GetClientSize()[0]-self.im_sizenwse.Width,self.GetClientSize()[1]-self.im_sizenwse.Width))

    def scaleMap(self,event):
        #print " event.GetWheelRotation()", event.GetWheelRotation()
        global SCREEN_SIZE
        if event.GetWheelRotation()<0 :
            if  self.scale*self.size[0]>IMAGE_MIN_SIZE and self.scale*self.size[1]>IMAGE_MIN_SIZE:
                self.scale=self.scale*(1-SCALE_SPEED)
                self.resizeMap(self.scale)
                #print "shang:",self.scale
        elif self.scale*self.size[0]< SCREEN_SIZE[0]*1.4 and self.scale*self.size[1]< SCREEN_SIZE[1]*1.4:
                self.scale=self.scale*(1+SCALE_SPEED)
                self.resizeMap(self.scale)
                #print "xia:",self.scale

    def OnMouseLeftDclick(self, event):
        if self.path!="imagePin.png":
            newSize=[50,50]
            minSize=60.0
            minScale=1
            mapSize=(self.im.Width,self.im.Height)
            if self.GetSize()[0]<=minSize or self.GetSize()[1]<=minSize:
                print self.im.Width
                tim=self.im.Copy().Rescale(self.im.Width,self.im.Height)
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
                tim=self.im.Copy().Rescale(int(self.im.Width*minScale),int(self.im.Height*minScale))
                self.bg.SetBitmap(wx.BitmapFromImage(tim))
                self.SetSize(newSize)
                newPos=[int(self.pos[0]+event.GetPosition()[0]-minSize/2),int(self.pos[1]+event.GetPosition()[1]-minSize/2)]#[int(self.pos[0]+mapSize[0]/2),int(self.pos[1]+mapSize[1]/2)]
                self.SetPosition(newPos)

                self.pos=newPos
                self.scale=minScale
                self.saveData()
            self.SetWindowShape(wx.BitmapFromImage(tim))
            self.b_sizenwse.SetPosition((self.GetClientSize()[0]-self.im_sizenwse.Width,self.GetClientSize()[1]-self.im_sizenwse.Width))


    def OnMouseLeftDown_size(self, event):
        self.lastPosSize[0]=wx.GetMousePosition()[0]
        self.lastPosSize[1]=wx.GetMousePosition()[1]
        self.b_sizenwse.CaptureMouse()

        pos= event.GetPosition()
        self.canSize=True
        self.canMove=False
    def OnMouseLeftUp_size(self, event):
        #self.canMove=False
        self.canSize=False
        if self.b_sizenwse.HasCapture():
            self.b_sizenwse.ReleaseMouse()
        tim=self.im.Copy().Rescale(self.GetClientSize()[0],self.GetClientSize()[1])
        self.bg.SetBitmap(wx.BitmapFromImage(tim))
        self.SetWindowShape(wx.BitmapFromImage(tim))
    def OnMouseLeftDown(self, event):
        self.lastPos[0]=wx.GetMousePosition()[0]
        self.lastPos[1]=wx.GetMousePosition()[1]
        self.bg.CaptureMouse()
        #self.pos=event.GetPosition()
        #pos= event.GetPosition()
        #self.canSize=False
        self.canMove=True

    def OnMouseLeftUp(self, event):
        self.canMove=False
        #self.canSize=False
        if self.bg.HasCapture():
            self.bg.ReleaseMouse()

    def close(self,event):
        if self.path!="imagePin.png":
            self.Close()


    def OnMoveSize(self,event):
        global IMAGE_MIN_SIZE
        newSizeX=int(wx.GetMousePosition()[0]-self.lastPosSize[0]+self.GetClientSize()[0])
        newSizeY=int(newSizeX/(self.size[0]/float(self.size[1])))
        newSize=(newSizeX,newSizeY)
        mineSize=IMAGE_MIN_SIZE
        if self.canSize and  newSize[0]>mineSize and  newSize[1]>mineSize:
            #tim=self.im.Copy().Rescale(newSizeX,newSizeY)
            #self.bg.SetBitmap(wx.BitmapFromImage(tim))
            #self.SetWindowShape(wx.BitmapFromImage(tim))
            self.SetSize(newSize)
            self.scale=newSize[0]/self.im.Width
            #print "f size:",newSize,"\n ","ture size:",self.GetClientSize()
        self.lastPosSize=wx.GetMousePosition()
        self.SetCursor(wx.StockCursor(wx.CURSOR_SIZENWSE))
        #self.b_sizenwse.SetPosition((self.GetClientSize()[0]-self.im_sizenwse.Width,self.GetClientSize()[1]-self.im_sizenwse.Width))

    def OnMove(self, event):
        #move pos
        newPosX=wx.GetMousePosition()[0]-self.lastPos[0]+self.pos[0]
        newPosY=wx.GetMousePosition()[1]-self.lastPos[1]+self.pos[1]
        newPos=(newPosX,newPosY)
        if self.canMove :
            self.SetPosition(newPos)
            self.pos=newPos
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.lastPos=wx.GetMousePosition()

        if event.GetPosition()[0]>self.GetClientSize()[0]-self.im_sizenwse.Width and  event.GetPosition()[1]>self.GetClientSize()[1]-self.im_sizenwse.Height:
            self.b_sizenwse.SetPosition((self.GetClientSize()[0]-self.im_sizenwse.Width,self.GetClientSize()[1]-self.im_sizenwse.Width))
        else:
            self.b_sizenwse.SetPosition((-self.im_sizenwse.Width,-self.im_sizenwse.Height))
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
        for s in ALL_FRAME:
           try:
               #print "name:",s.name
               s.saveData()
           except:
               ()
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
        grapStart()

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
        removeFile(self.path)
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
        showImageInDesktop(os.getcwd())

    def beWindowsPath(self,cPath):
        newPath=""
        for s in cPath:
            if s=="/":
                newPath+="/"
            else:
                newPath+=s
        return newPath

    def saveData(self):
        global MAIN_SETTINGS_TREE
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
            grapStart()

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
        #save_settings_data(MAIN_SETTINGS_TREE,settings_data)
    def changeToCN(self,evt):
        LANGUAGE_TYPE=1
        #save_settings_data(MAIN_SETTINGS_TREE,settings_data)



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
        #save_settings_data(MAIN_SETTINGS_TREE,settings_data)
        self.RemoveIcon()
        #self.frame.Close()
        if os.path.isfile("screen.png"):
            os.remove("screen.png")
        os.system("taskkill /f /im  ImagePin.exe &exit()")
        sys.exit()

    def showInExplorer(self, evt):
        os.popen("explorer "+os.getcwd())

    def grapScreen(self, evt):
        grapStart()

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

class grapingScreenFrame(wx.Frame):
    global ICON_PATH
    global SCREEN_SIZE
    global MAIN_SETTINGS_TREE
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id,'ImagePin',size=SCREEN_SIZE,style=wx.NO_BORDER|wx.STAY_ON_TOP|wx.FRAME_NO_TASKBAR)
        tBmp=wx.EmptyBitmap(600,600, depth=-1)
        self.SetSize(SCREEN_SIZE)

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

        #set icon
        try:
            self.tbicon = TB_Icon(self)
        except:
            self.tbicon = None

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

def createImagePinFrame(mapPath,state,pos,scale):
    startPos=wx.Point=(pos)
    pos[0]+=SCREEN_POS[0]
    pos[1]+=SCREEN_POS[1]
    tImage=wx.Image(mapPath,wx.BITMAP_TYPE_PNG)
    mapSize=tImage.GetSize()

    newFrame = grapPartFrame(parent=None, id=-1,imagePath=mapPath,im=wx.Image(mapPath,wx.BITMAP_TYPE_ANY))
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

def grap(box):
    global SAVE_SCREEN_MAP_PATH
    global GRAP_PF_NAME
    minSize=40
    if abs(box[2]-box[0])>=minSize and abs(box[3]-box[1])>=minSize:
        gTime=str(int(time.time()))
        save_path=ROOT_DIR+"\\"+GRAP_PF_NAME+"_"+gTime+".png"
        im = Image.open(SAVE_SCREEN_MAP_PATH)
        print SAVE_SCREEN_MAP_PATH
        imSize=()
        cim=Image.new('RGB',(abs(box[2]-box[0]),abs(box[3]-box[1])))
        region = im.crop(box)
        cim.paste(region, (0,0))
        cim.save(save_path)
        createImage(os.path.basename(save_path).replace(".png",""),True,[box[0],box[1]],1,save_path)


def createImage(name,state,pos,scale,mapPath):
	startPos=wx.Point=(pos)
	pos[0]+=SCREEN_POS[0]
	pos[1]+=SCREEN_POS[1]
	tImage=wx.Image(mapPath,wx.BITMAP_TYPE_ANY)
	mapSize=tImage.GetSize()
	newFrame = grapPartFrame(parent=None, id=-1,imagePath=mapPath,im=tImage)
	newFrame.pos=pos
	newFrame.miniState=state
	newFrame.scale=scale
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
	#newFrame.b_sizenwse.SetPosition((tSize[0]-newFrame.im_sizenwse.Width,tSize[1]-newFrame.im_sizenwse.Width))
	if state:
		newFrame.Show()
	else:
		newFrame.Hide()
	ALL_FRAME.append(newFrame)
	#print "\ncreateMap: " , "\n    name: ",name,"\n    path: ",mapPath
