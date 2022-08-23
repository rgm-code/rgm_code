

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import subprocess
import time
import tkinter.scrolledtext as tkscrolled



VERSION = '2.5.0'
if not os.path.isfile(os.path.expanduser('~/classes/version.txt')):
    if not os.path.isdir(os.path.expanduser('~/classes/')):
        os.mkdir(os.path.expanduser('~/classes/'))
    version_file = open(os.path.expanduser('~/classes/version.txt'), 'w')
    version_file.write(VERSION)
    version_file.close()
    
    import dau 

else:
    

    pass

window = tk.Tk()
window.title('RGM 2.5.0')
window.geometry('+%d+%d' % (window.winfo_screenwidth()/2, window.winfo_screenheight()/2))


root = ttk.Frame(window) 

root.pack(fill='both', expand=True)

tab = ttk.Notebook(root)
frame_main = ttk.Frame(tab)



h1 = window.winfo_screenwidth()/10/13
h1 = int(h1)
h2 = window.winfo_screenwidth()/10/16
h2 = int(h2)
h3 = h2

l1 = ttk.Label(frame_main, text='班級：')
l2 = ttk.Label(frame_main, text='每一組人數：')
var1 = tk.StringVar(frame_main)
e1 = ttk.OptionMenu(frame_main, var1)
var2 = tk.StringVar(frame_main)
var2.set('3')
e2 = ttk.Spinbox(frame_main, from_=2, to=50, width=2, textvariable=var2)

l3 = ttk.Label(frame_main, text='結果：')
show = tkscrolled.ScrolledText(frame_main, width=20, height=h1,
        font=('Helvetica', 13),
        state='disabled') 


l1.grid(padx=30, sticky='e')
l2.grid(row=1, column=0, padx=30, sticky='e')
e1.grid(row=0, column=1, sticky='w')
e2.grid(row=1, column=1, sticky='w')
l3.grid(row=2, sticky='e', padx=30, pady=(20, 5))
show.grid(row=3, column=0, columnspan=3, padx=(10, 0), sticky='we')

path = os.path.expanduser('~'+os.sep+'classes') 

seed0 = int(time.time()//3600*3600)
def get_group():
    import numpy as np
    global seed0
    cls_name = var1.get()
    np.random.seed(seed0-ord(cls_name[0]) % 2**32)

    

    try:
        num_people = int(e2.get())
    except ValueError:
        messagebox.showwarning('Error', '非數字輸入：%s' % e2.get(), parent=window)
        return

    cls_file = open(os.path.expanduser('~' + os.sep + 'classes' + os.sep + cls_name))
    

    cls_list = cls_file.readlines()
    cls_file.close()

    

    for n in range(len(cls_list)-1): 

        cls_list[n] = cls_list[n][:-1]

    

    num_student = len(cls_list)
    result = np.array(cls_list)
    for n in range(10):
        np.random.shuffle(result)
    result = np.resize(result, (num_student // num_people + 1, num_people))

    

    last = num_student % num_people
    if last == 0:
        result = np.delete(result, -1, axis=0)
    else:
        result[-1,last:] = ''

    

    result_text = ''
    for group in range(result.shape[0]):
        for people in range(result.shape[1]):
            if result[group, people] != '':
                result_text += str(result[group, people]) + ', '
        result_text += '\n-----------------------\n'
    
    show.configure(state='normal') 

    show.delete(1.0, tk.END)
    show.insert(tk.END, result_text)
    show.configure(state='disabled')

def get_group_event(event):
    return get_group()

def go_to_next(event):
    e2.focus_set()

start = ttk.Button(frame_main, text='開始分組', command=get_group)
start.grid(row=1, column=2, padx=30)

e1.bind('<Return>', go_to_next)
e2.bind('<Return>', get_group_event)



frame_add = ttk.Frame(tab)

lbox = tk.Listbox(frame_add)
lbox.grid(row=1, columnspan=2, padx=20, pady=10, sticky='ns')

l4 = ttk.Label(frame_add, text='學生名單')
l4.grid(row=0, column=1, columnspan=2)
text = tkscrolled.ScrolledText(frame_add, width=19, height=h2, font=('Helvetica', 16))
text.insert(1.0, '請先選擇班級')
text.configure(state='disable') 

text.grid(row=1, column=2, padx=20, pady=10)

from tkinter import simpledialog
def add():
    _cls_name = simpledialog.askstring(title='新增班級', prompt='班級名稱：')
    if _cls_name is not None:
        try:
            file = open(path+os.sep+_cls_name, 'w')
            file.close()
            update_cls_list(None) 

        except:
            pass

def delete():
    if lbox.get(tk.ANCHOR) != '': 

        is_sure = messagebox.askokcancel('', '是否刪除此班級？', parent=window)
        if is_sure:
            os.remove(path+os.sep+lbox.get(tk.ANCHOR)) 

            update_cls_list(None)

def save():
    if lbox.get(tk.ANCHOR) != '': 

        _content = text.get(1.0, tk.END)
        if _content[-1] == '\n':
            _content = _content[:-1] 


        fname = path+os.sep+lbox.get(tk.ANCHOR)
        file = open(fname, 'w')
        file.write(_content)
        file.close()

from time import sleep
import threading
def autosave(event):
    def _autosave():
        btn_save.configure(text='儲存中...')
        save()
        sleep(0.5)
        btn_save.configure(text='已更新：會自動儲存變更！')
    t = threading.Thread(target=_autosave)
    t.start()

text.bind('<KeyRelease>', autosave) 


btn_add = ttk.Button(frame_add, text='新增班級', command=add)
btn_add.grid(row=2, column=0, padx=10)
btn_del = ttk.Button(frame_add, text='移除班級', command=delete)
btn_del.grid(row=2, column=1, padx=10)
btn_save = ttk.Label(frame_add, text='已更新：會自動儲存變更！')
btn_save.grid(row=2, column=2, padx=10)

def load_cls_list(event):
    text.configure(state='normal')
    obj = event.widget
    index = obj.curselection()
    if index != (): 

        fname = obj.get(index)

        file = open(path+os.sep+fname, 'r')
        content = file.read()
        file.close()
        text.delete(1.0, tk.END) 

        text.insert(tk.END, content)
lbox.bind('<<ListboxSelect>>', load_cls_list)

def update_cls_list(event):
    try:
        file_list = os.listdir(path)
    except FileNotFoundError:
        os.mkdir(path)
        file_list = os.listdir(path) 


    if 'version.txt' in file_list: 

        file_list.remove('version.txt')
    if '.DS_Store' in file_list: 

        file_list.remove('.DS_Store')

    if file_list == []:
        e1 = ttk.OptionMenu(frame_main, var1, '無班級')
    else:
        e1 = ttk.OptionMenu(frame_main, var1, file_list[0], *file_list)
    e1.grid(row=0, column=1)

    lbox.delete(0, tk.END)
    lbox.insert(0, *file_list)
update_cls_list(None)
e1.bind('<Button-1>', update_cls_list)

tab.add(frame_main, text='分組')
tab.add(frame_add, text='編輯班級')
tab.pack(expand=1, fill='both')
tab.select(frame_main)

window.mainloop()
