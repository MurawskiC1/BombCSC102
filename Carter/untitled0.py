# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 22:31:34 2023

@author: carter.murawski
"""

import tkinter as tk
from tkinter import PhotoImage

def load_image():
    # Replace 'your_image_file.gif' with the path to your image file
    image_path = 'O.png'
    
    # Create a PhotoImage object
    img = PhotoImage(file=image_path)
    
    # Update the label's image
    label.config(image=img)
    
    # Keep a reference to the image to prevent it from being garbage collected
    label.image = img

# Create the main window
root = tk.Tk()
root.title("Image Viewer")

# Create a label to display the image
label = tk.Label(root)
label.pack(pady=10)

# Create a button to load the image
button = tk.Button(root, text="Load Image", command=load_image)
button.pack(pady=10)

# Run the Tkinter event loop