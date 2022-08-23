import requests
import os
import zipfile
import threading
from tkinter import *

download_url = 'https://xydp.000webhostapp.com/downloads/rgm_update.zip'

def dclose():
    root.protocol('WM_DELETE_WINDOW', 'a')

def aclose():
    root.protocol('WM_DELETE_WINDOW', lambda: root.destroy())

def update():
    btn.config(state=DISABLED)
    dclose() 


    def _update():
        try:
            lbl2.config(text='狀態：正在下載')
            f = requests.get(download_url)
            lbl2.config(text='正在寫入')

            path = os.path.expanduser('~/Desktop/')
            open(path+'rgm_update_download.zip', 'wb').write(f.content)
            lbl2.config(text='狀態：正在解壓縮')

            zfile = zipfile.ZipFile(path+'rgm_update_download.zip')
            zfile.extractall(path)
            os.chmod(path+'rgm_update', 0o744)
            os.remove(path+'rgm_update_download.zip')
            

            

            lbl2.config(text='狀態：初始化完成')
            aclose() 

        except requests.exceptions.RequestException:
            lbl1.config(text='抱歉，網路連線出現問題，請重新安裝')
            aclose()
            btn.config(state=NORMAL)

    t = threading.Thread(target=_update)
    t.start()

root = Tk()
root.geometry('400x200+500+200')
root.title('RGM 初始化')
lbl1 = Label(root, text='請先初始化（以後可以自動更新）', font=('Helvetica', 20))
lbl1.pack(pady=20)
btn = Button(root, text='開始', font=('Helvetica', 20), command=update)
btn.pack()
lbl2 = Label(root)
lbl2.pack()
root.mainloop()
