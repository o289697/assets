# -*- coding: utf-8 -*-

import os
import hashlib
from PIL import Image, ImageCms
import shutil
import ctypes


u="Administrator"

if os.name=="nt":
    path="C:\\Users\\"+u+"\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets\\"
else:
    path="/mnt/c/Users/"+u+"/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets"

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12
FOREGROUND_BLACK = 0x0
FOREGROUND_BLUE = 0x01 # text color contains blue.
FOREGROUND_GREEN= 0x02 # text color contains green.
FOREGROUND_RED = 0x04 # text color contains red.
FOREGROUND_INTENSITY = 0x08 # text color is intensified.
BACKGROUND_BLUE = 0x10 # background color contains blue.
BACKGROUND_GREEN= 0x20 # background color contains green.
BACKGROUND_RED = 0x40 # background color contains red.
BACKGROUND_INTENSITY = 0x80 # background color is intensified.
class Color:
    ''' See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winprog/winprog/windows_api_reference.asp
    for information on Windows APIs. - www.jb51.net'''
    if os.name=="nt":
        std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    else:
        std_out_handle = STD_OUTPUT_HANDLE
    def set_cmd_color(self, color, handle=std_out_handle):
        """(color) -> bit
        Example: set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        """ 
        return ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    def reset_color(self):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
    def print_red_text(self, print_text):
        self.echo(FOREGROUND_RED,print_text,"\033[31m")
    def print_green_text(self, print_text):
        self.echo(FOREGROUND_GREEN ,print_text,"\033[32m")    
    def print_red_text_with_blue_bg(self, print_text):
        self.echo(FOREGROUND_RED | FOREGROUND_INTENSITY | BACKGROUND_BLUE | BACKGROUND_INTENSITY,print_text ,"\033[1;31;44m")    
    def echo(self, color, print_text,color1):
        if os.name=="nt":
            self.set_cmd_color(color)
            print(print_text)
            self.reset_color()
        else:
            print(color1+print_text+"\033[0m")


def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myHash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myHash.update(b)
    f.close()
    return myHash.hexdigest() 

pics = {}
for root, _, files in os.walk(path):
    for name in files:
        pics[GetFileMd5(os.path.join(root, name))]=os.path.join(root, name)
'''
if not os.path.exists("log.txt"):
    open("log.txt", 'a').close()
file = open('log.txt', 'r')
exists = file.readlines()
for exist in exists:
    del pics[exist[:-1]]

file = open('log.txt', 'a')
for k,v in pics.items():
    file.write(k+"\n")
'''

if not os.path.exists("pic"):
    os.makedirs("pic") 
if not os.path.exists("pic/images"):
    os.makedirs("pic/images") 
if not os.path.exists("pic/trash"):
    os.makedirs("pic/trash") 
'''
ext={
    'JPEG':'jpg',
    'PNG':'png',
    'GIF':'gif'
}
'''

L1=[]
L2=[]
for k,v in pics.items():
    try:
        img = Image.open(v)  
        file=""      
        if img.size[0]>1100:
            file="pic/images/"+k+"."+img.format.lower()
        else:
            file="pic/trash/"+k+"."+img.format.lower()
        if not os.path.exists(file):
            L1.append(file)
            shutil.copy(v,file)
            try:
                print(os.remove(v))
            except OSError:
                None
            except:
                None
    except:
        L2.append(os.path.basename(v))

clr = Color()
for f in L1:
    clr.print_green_text(f)
print(len(L1))
for f in L2:
    clr.print_red_text(f)     
print(len(L2))

clr.print_red_text_with_blue_bg("========")

if os.name=="nt":
    if (len(L1)+len(L2)) > 0 :
        os.system("explorer "+path)
    #print("explorer "+path)
    os.system("pause")




        




