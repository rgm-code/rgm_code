import requests
import os
import zipfile
import threading
from tkinter import *
import subprocess
import time




version_url = 'https://xydp.000webhostapp.com/downloads/version.txt'
download_url = 'https://xydp.000webhostapp.com/downloads/rgm-'
new_version = requests.get(version_url).text

def dclose():
    root.protocol('WM_DELETE_WINDOW', 'a')

def aclose():
    root.protocol('WM_DELETE_WINDOW', lambda: root.destroy())

def update():
    global new_version
    btn.config(state=DISABLED)
    dclose() 


    def _update():
        try:
            path = os.path.expanduser('~/Desktop/')
            os.remove(path+'RGM')
            lbl2.config(text='狀態：正在下載')
            f = requests.get(download_url + new_version + '.zip')
            lbl2.config(text='正在寫入')

            with open(path+'rgm_download.zip', 'wb') as df:
                df.write(f.content)
            lbl2.config(text='狀態：正在解壓縮')

            subprocess.run(['open', path+'rgm_download.zip'])
            while not os.path.isfile(path+'RGM'):
                time.sleep(1) 

            lbl2.config(text='狀態：安裝完成')
            lbl1.config(text='點擊桌面上的「RGM」開啟新版本')
            aclose() 

        except requests.exceptions.RequestException:
            lbl1.config(text='抱歉，網路連線出現錯誤，請重新安裝')
            aclose()
            btn.config(state=NORMAL)

    t = threading.Thread(target=_update)
    t.start()

try:
    with open(os.path.expanduser('~/classes/version.txt'), 'r') as f:
        current_version = f.read()
except FileNotFoundError:
    os.sys.exit()

def isnew(old, new):
    _old = [int(old[0]), int(old[2]), int(old[4])]
    _new = [int(new[0]), int(new[2]), int(new[4])]
    for i in range(3):
        if _new[i] > _old[i]:
            return True
        elif _new[i] < _old[i]:
            return False
        else:
            continue
    return False

path = os.path.expanduser('~/Desktop/')


if True:
    root = Tk()
    root.geometry('400x200+500+200')
    root.title('RGM 自動更新')
    lbl1 = Label(root, text='RGM 有可用的更新：版本%s！' % new_version, font=('Helvetica', 20))
    lbl1.pack(pady=20)
    btn = Button(root, text='立即更新', font=('Helvetica', 20), command=update)
    btn.pack()
    lbl2 = Label(root)
    lbl2.pack()
    root.mainloop()
    os.remove(path+'rgm_download.zip')
