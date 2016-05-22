# -*- coding: utf-8 -*-
import sys,os,wx
from  xml.etree.ElementTree import*
reload(sys)
sys.setdefaultencoding( "utf-8" )
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
SCREEN_SIZE=(1920,1080)

SCALE_SPEED=0.1
ADJUST_SCALE_SPEED=0.04
IMAGE_MAX_SIZE=4000
IMAGE_MIN_SIZE=30
IMAGE_SCALE_MIN_MAX=[0.04,12]

TEST_FRAME=[]

MAINFRAME=[]

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

#mainFrame=None
#import pyautogui


#pyautogui.confirm(text='', title='', buttons=range(10))
# pyautogui.screenshot("ss.png")
# pyautogui.moveTo(10,1)
