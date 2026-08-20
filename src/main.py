import os
import shutil


def copydir(srcpath:str, destpath:str):
    listdir = os.listdir(srcpath)
    for item in listdir:
        print(srcpath+"/"+item)
        if os.path.isfile(srcpath+"/"+item):
            shutil.copy(srcpath+"/"+item, destpath+"/"+item)
        if os.path.isdir(srcpath+"/"+item):
            os.mkdir(destpath+"/"+item)
            copydir(srcpath+"/"+item, destpath+"/"+item)

def copy_new():
    if os.path.exists("./public"):
        print("deleting Public")
        shutil.rmtree("./public")
        print("Creating Public")
    os.mkdir("./public")
    print("copying...")
    copydir("./static", "./public")
    print("done!")





def main():
    copy_new()



main()
