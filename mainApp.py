from  ShowImage import*
from _imagePinUtil import *
import _globalData


def start():
    global ROOT_DIR
    global settings_data
    global MAINFRAME

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
        #print "pos:",pos
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


if __name__ == '__main__':
    if  os.path.isfile(SET_FILE_PATH)==False:
        createSetingsFile()
    MAIN_SETTINGS_TREE=ElementTree(file=SET_FILE_PATH).getroot()

    #error get_settings_data(MAIN_SETTINGS_TREE,settings_data)

    LANGUAGE_PACK=LANGUAGE_PACK_ALL[settings_data["LANGUAGE_TYPE"]]


    mainApp = wx.App()
    SCREEN_SIZE=wx.GetDisplaySize()
    bmp=wx.EmptyBitmap(10,10, depth=-1)
    mainFrame=grapingScreenFrame(parent=None, id=-1)
    #mainFrame=grapingScreenFrame(parent=None, id=-1)
    mainFrame.bg.SetBitmap(bmp)
    MAINFRAME.append(mainFrame)
    imagePin_Path="imagePin.png"
    imagePin_Pos=[100,100]
    imagePinFrame=createImagePinFrame(imagePin_Path,True,imagePin_Pos,1)
    #imagePinFrame=createImagePinFrame(imagePin_Path,True,imagePin_Pos,1)
    # createMap("noname_paste",True,(100,100),1,1,"imagePin")\

    #createImage("noname",True,imagePin_Pos,1,imagePin_Path)
    #createImage("1",True,[200,200],1,"demo.png")
    #createImage("1",True,[300,200],1,"demo1.png")
    #createImage("1",True,[400,200],1,"demo2.png")
    #createImage("1",True,[500,200],1,"demo3.png")
    #createImage("1",True,[600,200],1,"demo3.jpg")
    #createImage("1",True,[500,500],1,"1.png")
    #createImage("1",True,[500,500],1,"2.png")

    #testFrame=textFrame(parent=None,id=-1,text="xxxxxxxxxxxxxxx")
    #testFrame.Show()

    start()

    mainApp.MainLoop()
