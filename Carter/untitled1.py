# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 15:44:58 2023

@author: carter.murawski
"""

from tkinter import *
import tkinter

def hello():
    note = Label(window, text="Hello")
    note.pack()
    
    
window = Tk()
label = tkinter.Button(window,text="BEGIN",command = hello())
label.pack()
