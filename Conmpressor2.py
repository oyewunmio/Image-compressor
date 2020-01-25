#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 18:15:48 2019

@author: oyewunmi
"""

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
import os
import secrets
import time
import timeit
from PIL import Image
from tkinter import messagebox as msgbox

class Compressor(tk.Tk):
    'Main class container for the compressor'
    def __init__(self, *args, **kwargs):
        'Class constructor'
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Image Compressor')
        self.geometry('%dx%d+%d+%d' % (400, 300, 0, 0))
        self.files = tk.StringVar()
        self.file = ''
        self.WrkDir = os.path.dirname(__file__)
        self.Window()
        self.Time_to_run()
    
    def FileOpenCallbck(self):
        'Callback for the first button to open the open file dialog'
        files_ext = [('JPG', '*.jpg'), ('PNG', '*.png')]
        self.file = fd.askopenfilename(parent = self, filetypes = files_ext, defaultextension = files_ext, initialdir=self.WrkDir)
        self.file1 = os.path.split(self.file)[1]
        self.files.set(self.file1)
        self.type_lab.config(text = '{}'.format(os.path.splitext(self.file)[1]))
        self.size_lab.config(text = '{0:.2f} mb'.format(int(os.stat(self.file).st_size)/1048576))
        
    def pic_compress(self):
        'This is a function that takes in a picture and decompresses it'
        Compressed_folder = os.path.join(self.WrkDir + '/compressed')
        if Compressed_folder:
            if not os.access(Compressed_folder, os.F_OK) : os.mkdir(Compressed_folder)
        random_hex = secrets.token_hex(6)
        ext = os.path.splitext(self.file)
        picture_name = random_hex + ext[1]
        picture_path = os.path.join(self.WrkDir,'compressed/',picture_name)
        output_size = (120, 120)
        try:
            i = Image.open(self.file) 
            i.thumbnail(output_size)
            i.save(picture_path)
            self.ProgressBar()
        except AttributeError:
            return 1
       
    
    def ProgressBar(self):
        'This is the callback for the progress bar'
        self.progress_Bar['maximum'] = 100
        for i  in range(100):
            time.sleep(self.time_taken/100)
            self.progress_Bar['value'] = i
            self.progress_Bar.update()
            self. progress_Bar['value'] = 0
        msgbox.showinfo(message='Compressing image is done')
           
    def Time_to_run(self):
         Code_to_test ="""def pic_compress(input_pic):
            random_hex = secrets.token_hex(6)
            ext = os.path.splitext(input_pic)
            picture_name = random_hex + ext[1]
            picture_path = os.path.join(Wrk_dir,'compressed/',picture_name)
            output_size = (120, 120)
            i = Image.open(input_pic) 
            i.thumbnail(output_size)
            i.save(picture_path)
            return picture_name
        """
         self.time_taken = timeit.timeit(Code_to_test)

    
    def Security(self):
        'This ensures that a file is choosen before the compress button can be clicked'
        if self.file == '' or None:
#            self.Comp_but.config(state='disabled')
            msgbox.showerror(message='No image file is been selected')
        
       
    def Window(self):
        'Application window'
        self.Frame1 = ttk.LabelFrame(self, text='Manage files')
        self.Frame1.grid(column=0, row=1, sticky='WE', padx=10, pady=5)
        self.Frame2 = ttk.LabelFrame(self, text='Preview')
        self.Frame2.grid(column=1, row=1, sticky='WE', padx=10, pady=5)
        
        #Putting the widgets into the first frame
        self.But1 = ttk.Button(self.Frame1, text='Browse to file:', command=self.FileOpenCallbck)
        self.But1.grid(row=1, column=1, padx=10)
        self.file_Entry = ttk.Entry(self.Frame1, width=30, textvariable=self.files)
        self.file_Entry.grid(row=1, column=2, pady=20, padx=10)
        self.file_Entry.config(state='readonly')
        ttk.Label(self.Frame1, text='File Type:').grid(row=3, column=1, padx=5, pady=2)
        ttk.Label(self.Frame1, text='File Size:').grid(row=4, column=1, padx=5, pady=2)
        self.Comp_but = ttk.Button(self.Frame1, text='Compress File', command=lambda: [self.Security(), self.pic_compress()])
        self.Comp_but.grid(row=5, column=2, pady=5)
        self.type_lab = ttk.Label(self.Frame1, text='')
        self.type_lab.grid(row=3, column=2, padx=5, pady=2)
        self.size_lab = ttk.Label(self.Frame1, text='')
        self.size_lab.grid(row=4, column=2, padx=5, pady=2)
        self.progress_Bar = ttk.Progressbar(self.Frame1, orient='horizontal', length=300, mode='determinate')
        self.progress_Bar.grid(column=2, row=6, padx=7, pady=3)
    
            
Compressor().mainloop()