import os,sys
helpInfor="do not kick me! drag *.py to me!"
try:
    sys.argv[1]
except:
    print helpInfor
    raw_input("press  Enter to Exit!")
else:
    if sys.argv[1][:2]=="-c":
        if sys.argv[1][2:]!="":
            print "\n",os.path.dirname(sys.argv[1][2:]),"\n"
            os.chdir(os.path.dirname(sys.argv[1][2:]))
            cmd = "python c:\\PyInstaller2.1\\pyinstaller.py " +sys.argv[1][2:]+ " -F --icon=c:\\PyInstaller2.1\\GOM.ico"
            print cmd
            os.system(cmd)
        else:
            print helpInfor
            raw_input("press  Enter to Exit!")
    else:
    	print "\n",os.path.dirname(sys.argv[1]),"\n"
        os.chdir(os.path.dirname(sys.argv[1]))
        cmd = "python c:\\PyInstaller2.1\\pyinstaller.py " +sys.argv[1]+ " -w -F --icon=c:\\PyInstaller2.1\\GOM.ico"
        print cmd
        os.system(cmd)
        raw_input("press  Enter to Exit!")