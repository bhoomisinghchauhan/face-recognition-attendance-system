from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np

class Face_Recognition:

    def __init__(self, root):

        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1500x700")
        self.root.resizable(False, False)

        # background
        bg_img = Image.open("images/bg.png").resize((1500, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(bg_img)

        self.canvas = tk.Canvas(root,width=1500,height=750,highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")






if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()