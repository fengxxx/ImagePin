import os,sys

platform=sys.platform
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
#
#
# from Cocoa import *
# import Cocoa
# def evthandler(event):
#   pass # this is where you do stuff; see NSEvent documentation for event
# observer = Cocoa.NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSKeyDown, evthandler)
# # when you're done
# Cocoa.NSEvent.removeMonitor_(observer)
#
# import Quartz
# def evthandler(proxy, type, event, refcon):
#     pass # Here's where you do your stuff; see CGEventTapCallback
#     return event
# source = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateHIDSystemState)
# tap = Quartz.CGEventTapCreate(Quartz.kCGSessionEventTap,
#                               Quartz.kCGHeadInsertEventTap,
#                               Quartz.kCGEventTapOptionListenOnly,
#                               (Quartz.CGEventMaskBit(Quartz.kCGEventKeyDown) |
#                                Quartz.CGEventMaskBit(Quartz.kCGEventKeyUp)),
#                               handler,
#                               refcon)
