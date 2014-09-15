import os,sys
helpInfor="do not kick me! drag *.py to me!"
try:
    sys.argv[1]
except:
    print helpInfor
    raw_input("press  Enter to Exit!")
else:
    print sys.argv,"\n\n"+sys.argv[1][:3]+"\n\n"
    if sys.argv[1]!="" and sys.argv[1][(len(sys.argv[1])-2):]==".c":
        root_dir=os.path.dirname(sys.argv[1])
        print "\nroot_dir:  ",root_dir,"\n"
        os.chdir(root_dir)
        out_path=sys.argv[1].replace(".c","exe")
        cmd = "gcc -o " +out_path+" "+sys.argv[1] +" & "+out_path+"&pause"
        
        print cmd,"\n\n"
        os.system(cmd)
    else:
        print helpInfor
        raw_input("press  Enter to Exit!")