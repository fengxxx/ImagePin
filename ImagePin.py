#!/usr/bin/env python
# -*- coding: cp936 -*-
import Image
import win32api,win32con ,win32ui,win32gui
from  xml.etree.ElementTree import*
import wx
import os,sys,time 
import string
import win32pdh

ROOT_DIR=os.getcwd()
#ROOT_DIR="K:\\temp\\screenGrap_Fengx\\"
ICON_PATH=ROOT_DIR+"\\app.ico"
SAVE_GRAP_MAP_PATH=ROOT_DIR+"\\fengx.png"
SAVE_SCREEN_MAP_PATH=ROOT_DIR+"\\screen.png"
GRAP_PF_NAME="ThreeKindom"
CAN_GRAP=True

GRAP_RECT=[1,1,2,2]

# get the screen size (support multiply display)
	
	#get single display size 
	#SCREEN_SIZE=(win32api.GetSystemMetrics(win32con.SM_CXSCREEN),win32api.GetSystemMetrics(win32con.SM_CYSCREEN))

SCREEN_POS=(0,0)
SCREEN_SIZE=(100,100)



def GetProcessID( name ):
    object = "Process"
    items, instances = win32pdh.EnumObjectItems(None,None,object, win32pdh.PERF_DETAIL_WIZARD)
    val = None
    if name in instances :
        hq = win32pdh.OpenQuery()
        hcs = []
        item = "ID Process"
        path = win32pdh.MakeCounterPath( (None,object,name, None, 0, item) )
        hcs.append(win32pdh.AddCounter(hq, path))
        win32pdh.CollectQueryData(hq)
        time.sleep(0.01)
        win32pdh.CollectQueryData(hq)
        for hc in hcs:
            type, val = win32pdh.GetFormattedCounterValue(hc, win32pdh.PDH_FMT_LONG)
            win32pdh.RemoveCounter(hc)
            win32pdh.CloseQuery(hq)
            return val

def GetAllProcesses():
	object = "Process"
	items, instances = win32pdh.EnumObjectItems(None,None,object, win32pdh.PERF_DETAIL_WIZARD)
	return instances



#get screnPos and max size
def getScreenSizePos():
	global SCREEN_POS
	global SCREEN_SIZE
	MoniterDev=win32api.EnumDisplayMonitors(None,None)	
	if len(MoniterDev)==1:
		SCREEN_POS=(MoniterDev[1][2][0],MoniterDev[1][2][1])
		SCREEN_SIZE=(MoniterDev[1][2][2],MoniterDev[1][2][3])

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
		SCREEN_POS=(min(ax),min(ay))
		SCREEN_SIZE=((max(ax)-min(ax)),(max(ay)-min(ay)))



#  -------------- xml

SET_FILE_PATH="sttings.fengx"
MAIN_SETTINGS_TREE=ElementTree("root")

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


def createSetingsFile():
	global ROOT_DIR
	global GRAP_PF_NAME
	t=Element("root")
	#t.text="fengx"
	files= os.listdir(ROOT_DIR)
	fElement=[]
	i=1
	for m in files:
		nameParts=string.split(os.path.basename(m),"_")
		print nameParts
		if nameParts[0]==GRAP_PF_NAME:
			if os.path.splitext(m)[1]==".png":
				fElement.append(grapPartElement(m,True,[10,10],1))
	for s in fElement:
		t.append(s)

	settings=ElementTree("fengxx")
	settings._setroot(indent(t))
	settings.write(SET_FILE_PATH,"utf-8")



if  os.path.isfile(SET_FILE_PATH):
	MAIN_SETTINGS_TREE=ElementTree(file=SET_FILE_PATH).getroot()
else:
	createSetingsFile()
	MAIN_SETTINGS_TREE=ElementTree(file=SET_FILE_PATH).getroot()



def saveChange(mainTree,name,s,pos,sc):
	print mainTree,name,s,pos,sc
	sTree=grapPartElement(name,s,pos,str(sc))

	if mainTree.find(name)!=None:
		mainTree.remove(mainTree.find(name))
	mainTree.append(sTree)

	settings=ElementTree("fengx")
	settings._setroot(indent(mainTree))
	settings.write(SET_FILE_PATH,"utf-8")



# tabbar icon class
class TB_Icon(wx.TaskBarIcon):
	global ICON_PATH
	global ALL_FRAME
	m_close=wx.NewId()
	m_seting=wx.NewId()
	m_hide=wx.NewId()
	m_show=wx.NewId()
	m_screenGrap=wx.NewId()
	m_DeleteAll=wx.NewId()
	m_reset=wx.NewId()
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
	def CreatePopupMenu(self):
		menu= wx.Menu()
		menu.Append(self.m_show, "Show all window") 
		menu.Append(self.m_hide,  "Hide all window")
		menu.Append(self.m_reset,"resetPosition")
		menu.AppendSeparator()
		menu.Append(self.m_screenGrap, "Grap")
		menu.Append(self.m_DeleteAll, "Delete All DATA")
		menu.Append(self.m_close, "Exit")
		
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
	def reset(self,evt):
		i=0
		for s in ALL_FRAME:
			i+=1
			try:
				#s.show()
				a=1
				s.scale=0.4
				
				s.pos=[i*60,i*60]
				s.miniState=False
				s.SetPosition(s.pos)
				s.resizeMap(s.scale)
			except :
				print ""
		#os.remove(SET_FILE_PATH)

		#MAIN_SETTINGS_TREE=Element(" ")
		#start()
	def showALL_FRAME(self,evt):
		for s in ALL_FRAME:
			try:
				s.Show()
			except ImportError:
				print ""
	def hideALL_FRAME(self,evt):
		for s in ALL_FRAME:   
			try:
				s.Hide()
			except ImportError:
				print ""
		
	def closeApp(self, evt):
		for s in ALL_FRAME:
			try:
				s.saveData()
			except:
				print "guo"
		self.RemoveIcon()
		#self.frame.Close()
		sys.exit()
		
	def grapScreen(self, evt):
		grapStart(bmp)

	def onDeleteAll(self, event):
		global ROOT_DIR
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
					print ""
			for m in files:
				if os.path.splitext(m)[1]==".png" :#or os.path.splitext(m)[1]==".fengx":
					os.remove(m)

		dlg.Destroy()  


class grapingScreenFrame(wx.Frame):
	global ICON_PATH
	global SAVE_GRAP_MAP_PATH
	
	global SCREEN_SIZE
	print SCREEN_SIZE
	global MAIN_SETTINGS_TREE
	def __init__(self, parent, id):
		wx.Frame.__init__(self, parent, id,'null',size=SCREEN_SIZE ,style=wx.SIMPLE_BORDER|wx.STAY_ON_TOP)
		tBmp=wx.EmptyBitmap(10,10, depth=-1)
		self.SetSize(SCREEN_SIZE)
		self.bg=wx.StaticBitmap(self,-1,  tBmp, (0,0))
		self.bg.Bind(wx.EVT_LEFT_UP, self.OnLeftMouseUp)
		self.bg.Bind(wx.EVT_LEFT_DOWN, self.OnLeftMouseDown)
		self.bg.Bind(wx.EVT_MIDDLE_UP,  self.close)
		self.bg.Bind(wx.EVT_RIGHT_DOWN,  self.close)
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
			grap(GRAP_RECT,SAVE_GRAP_MAP_PATH)
			self.Hide()
		
	def close(self,event):
		self.Hide()

class grapPartFrame(wx.Frame):
	global SCREEN_SIZE
	global SCREEN_POS
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
		wx.Frame.__init__(self, parent, id, 'fengx', size=SCREEN_SIZE,style=wx.SIMPLE_BORDER|wx.STAY_ON_TOP)
		#self.bg=wx.StaticBitmap(self,-1,  wx.EmptyBitmap(10,10, depth=-1), (0,0))

		tBmp=wx.EmptyBitmap(10,10, depth=-1)

		self.bg=wx.StaticBitmap(self,-1,  tBmp, (0,0))
		self.bg.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
		self.bg.Bind(wx.EVT_LEFT_DCLICK, self.OnMouseLeftDclick)
		self.bg.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
		self.bg.Bind(wx.EVT_MOTION,  self.OnMove)
		self.bg.Bind(wx.EVT_MIDDLE_UP,  self.onHide)
		self.Bind(wx.EVT_MOUSEWHEEL, self.scaleMap)
		self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
	   
		#self.p=wx.Panel   
		#self.p.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)	
	
	def resizeMap(self,sc):
		im=wx.Image(self.name)
		size=im.GetSize()
 
		tSize=(size[0]*self.scale,size[1]*self.scale)
		tim=im.Rescale(size[0]*self.scale,size[1]*self.scale)
		self.bg.SetBitmap(wx.BitmapFromImage(tim))  
		self.SetSize(tSize)

	def scaleMap(self,event):
		global SCREEN_SIZE
		im=wx.Image(self.name)
		size=im.GetSize()
		sSize=30
		if event.GetWheelRotation()<0:
			if  self.scale*size[0]>sSize and self.scale*size[1]>sSize:
				self.scale=self.scale*0.9
				self.resizeMap(self.scale)
		else: 
			if  self.scale*size[0]< SCREEN_SIZE[0]*1.4 and self.scale*size[1]< SCREEN_SIZE[1]*1.4:
				self.scale=self.scale*1.1
				self.resizeMap(self.scale)


	def OnMouseLeftDclick(self, event):  
		im=wx.Image(self.name) 
		newSize=(50,50)
		minSize=60.0
		minScale=1
		mapSize=(im.Width,im.Height)
		#print ("Mouse pos"+str(event.GetPosition()))

		if self.GetSize()[0]<=minSize or self.GetSize()[1]<=minSize:
			tim=im.Rescale(im.Width,im.Height)
			self.bg.SetBitmap(wx.BitmapFromImage(tim))  
			self.SetSize((im.Width,im.Height))
			newPos=[int(self.pos[0]+event.GetPosition()[0]-mapSize[0]/2),int(self.pos[1]+event.GetPosition()[1]-mapSize[1]/2)]
			self.SetPosition(newPos)
			print newPos
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
			print newPos
			self.SetPosition(newPos)

			self.pos=newPos
			self.scale=minScale
			self.saveData()
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
		
		#print IsShown(self)
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
		#print ("OnContextMenu\n")

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

			self.Bind(wx.EVT_MENU, self.onSave, id=self.pp_SAVE)
			self.Bind(wx.EVT_MENU, self.onClose, id=self.pp_CLOSE)
			self.Bind(wx.EVT_MENU, self.onHide, id=self.pp_HIDE)
			self.Bind(wx.EVT_MENU, self.onDelete, id=self.pp_DELETE)	
			self.Bind(wx.EVT_MENU, self. grapScreen, id=self.pp_GRAP)

		menu = wx.Menu()

		menu.Append(self.pp_GRAP,"&Grap")
		item = wx.MenuItem(menu, self.pp_SAVE,"&Save")
		bmp=wx.BitmapFromIcon(wx.Icon(os.getcwd()+'\\App.ico'))
		#item.SetBitmap(bmp)
		menu.AppendItem(item)

		menu.Append(self.pp_CLOSE, "&Close")
		menu.Append(self.pp_HIDE, "&Hide")
		menu.Append(self.pp_DELETE, "&Delete")
		#sm = wx.Menu()
		#sm.Append(self.pp_TEST, "ThreeKindom")
		#sm.Append(self.pp_TEST, "ZHOU")
		#menu.AppendMenu(self.pp_TEST, "RuangJi", sm)

		self.PopupMenu(menu)
		menu.Destroy()

	def grapScreen(self, evt):
		grapStart(bmp)
	def onSavee(self, event):
		
		wildcard = "Python source (*.png)|*.png|"	 \
		   "All files (*.*)|*.*"

		dlg = wx.FileDialog(
			self, message="Save file as ...", defaultDir=os.getcwd(), 
			defaultFile="", wildcard=wildcard, style=wx.SAVE
			)

		print dlg.GetPath()
		dlg.SetFilterIndex(2)
		print dlg.GetPath()
		if dlg.ShowModal() == wx.ID_OK:
			if os.path.isdir(dlg.GetPath()):
				copyFiles(self.name, dlg.GetPath())
		dlg.Destroy()

	def onSave(self,event):
		global SAVE_GRAP_MAP_PATH
		wildcard = "Python source (*.png)|*.png|"	 \
		"All files (*.*)|*.*"
		dialog=wx.FileDialog(self, message="Save file as ...", defaultDir=os.getcwd(), 
		defaultFile=self.name, wildcard=wildcard,style=wx.SAVE)

		tPath=os.path.dirname(self.name) 
		if dialog.ShowModal()==wx.ID_OK:			
			#print tPath
			#print  dialog.GetPath()
			#print os.path.isdir(self.beWindowsPath(tPath))
			#if os.path.isdir(self.beWindowsPath(tPath)):
			os.system ("copy %s %s" % (tPath, dialog.GetPath()))


		#dialog.destory()
	def onClose(self, event):
		self.saveData()
		self.Close()

	def onHide(self, event):
		self.miniState=False
		self.saveData()
		self.Hide()

	def onDelete(self, event):
		os.remove(self.name)
		self.Close()

	def onDeleteAll(self, event):
		global ROOT_DIR
		files= os.listdir(ROOT_DIR)
		for s in ALL_FRAME:
			try:
				s.Hide()
				s.Close()
			except ImportError:
				print ""
		for m in files:
			if os.path.splitext(m)[1]==".png":
				os.remove(m)

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
		print "saveData",MAIN_SETTINGS_TREE,self.name,self.miniState,self.pos,self.scale
		
		saveChange(MAIN_SETTINGS_TREE,self.name,self.miniState,self.pos,self.scale)

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
	
	#name=os.path.basename(mapPath)
	#print name 
	newFrame.name=os.path.basename(mapPath)
	newFrame.SetSize(mapSize)
	#print startPos
	newFrame.SetPosition(startPos)
	newFrame.bg.SetBitmap(wx.BitmapFromImage(tImage))

	tSize=(newFrame.GetSize()[0]*scale,newFrame.GetSize()[1]*scale)
	tim=tImage.Rescale(newFrame.GetSize()[0]*newFrame.scale,newFrame.GetSize()[1]*scale)
	newFrame.bg.SetBitmap(wx.BitmapFromImage(tim))  
	newFrame.SetSize(tSize)

	'''
	LOG=""
	LOG+=mapPath+str(state)+str(pos)+str(scale)
	print LOG
	print mapPath,state,pos,scale 
	'''

	saveChange(MAIN_SETTINGS_TREE,newFrame.name,state,pos,scale)
	if state:
		newFrame.Show()
	else:
		newFrame.Hide()
	ALL_FRAME.append(newFrame)
		
def grap(box,sPath):

	global SAVE_SCREEN_MAP_PATH
	global GRAP_PF_NAME
	minSize=40
	if abs(box[2]-box[0])>=minSize and abs(box[3]-box[1])>=minSize:
		gTime=str(int(time.time()))
		sPath=os.path.dirname(sPath)+"\\"+GRAP_PF_NAME+"_"+gTime+".png"

		im = Image.open(SAVE_SCREEN_MAP_PATH)
		imSize=()
		cim=Image.new('RGB',(abs(box[2]-box[0]),abs(box[3]-box[1])))
		region = im.crop(box)
		cim.paste(region, (0,0))
		cim.save(sPath)
		createMap(sPath,True,[box[0],box[1]],1)

def screenCapture(savePath,size):
	getScreenSizePos()
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
	getScreenSizePos()
	global SCREEN_SIZE
	global SAVE_SCREEN_MAP_PATH
	screenCapture(SAVE_SCREEN_MAP_PATH,SCREEN_SIZE)
	tImage=wx.Image(SAVE_SCREEN_MAP_PATH,wx.BITMAP_TYPE_PNG)
	mainFrame.bg.SetBitmap(wx.BitmapFromImage(tImage))
	mainFrame.Show()

		
def start():
	getScreenSizePos()

	global ROOT_DIR
	LOG=""
	files= os.listdir(ROOT_DIR)
	i=1
	for m in files:
		nameParts=string.split(os.path.basename(m),"_")
		if nameParts[0]==GRAP_PF_NAME:
			if os.path.splitext(m)[1]==".png":
				tTree=MAIN_SETTINGS_TREE.find(os.path.basename(m))
				LOG+="\nname: "+m
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
				#print LOG
	#for s in ALL_FRAME:
	#	s.saveData()


softOn=True

i=0
if softOn:
	for s in  GetAllProcesses():
		softOn=False
		if s=="ImagePin":
			i+=1
	if i>2:
		sys.close()


getScreenSizePos()
ALL_FRAME=[]
mainApp = wx.PySimpleApp()
bmp=wx.EmptyBitmap(10,10, depth=-1)
mainFrame=grapingScreenFrame(parent=None, id=-1)
mainFrame.bg.SetBitmap(bmp)
start()

mainApp.MainLoop()

#---------global key

