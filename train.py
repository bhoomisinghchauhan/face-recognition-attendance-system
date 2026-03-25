from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np

class Train:

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

        # title
        self.canvas.create_text(
            750,
            60,
            text="Train Data Set",
            font=("Segoe UI", 36, "bold"),
            fill="white"
        )

        # =========================
        # TOP IMAGE (Recognition)
        # =========================

        # increased width only
        recog_img = Image.open("images/recognition.png").resize((1200,240), Image.LANCZOS)
        self.recog = ImageTk.PhotoImage(recog_img)

        self.canvas.create_image(
            750,
            250,   # moved down to create space
            image=self.recog
        )

        # =========================
        # TRAIN BUTTON
        # =========================

        train_btn = Button(
            root,
            text="Train Now",
            font=("Segoe UI",18,"bold"),
            bg="red",
            fg="white",
            command=self.train_classifier,
            activebackground="#b30000",
            activeforeground="white",
            cursor="hand2",
            bd=0,
            padx=40,
            pady=10
        )

        self.canvas.create_window(
            750,
            380,
            window=train_btn
        )

        # =========================
        # LOWER IMAGE
        # =========================

        # increased width only
        server_img = Image.open("images/client_server.png").resize((1200,240), Image.LANCZOS)
        self.server = ImageTk.PhotoImage(server_img)

        self.canvas.create_image(
            750,
            500,
            image=self.server
        )

    # function
    def train_classifier(self):
        data_dir = ("data")
        path = [os.path.join(data_dir,file) for file in os.listdir(data_dir)]
        
        faces =[]
        ids = []

        for image in path:
            img = Image.open(image).convert('L')      #gray scale image
            imageNp = np.array(img,'uint8')
            id = int(os.path.split(image)[1].split('.')[1])

            faces.append(imageNp)
            ids.append(id)

            cv2.imshow("Training",imageNp)
            cv2.waitKey(1) == 13
        ids = np.array(ids)

        # train the classifier and save
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces,ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Result","Training datasets completed !!")






if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()