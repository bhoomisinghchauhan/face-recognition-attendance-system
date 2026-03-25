import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Toplevel
import os
from tkinter import messagebox
from student import Student
from train import Train
from face_recognition import Face_Recognition


class FaceRecognitionUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1500x700")
        self.root.resizable(False, False)

        # background

        bg_img = Image.open("images/bg.png").resize((1500, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(bg_img)

        self.canvas = tk.Canvas(root, width=1500, height=750, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")

        # title

        self.canvas.create_text(
            750,
            60,
            text="Face Recognition Attendance System Software",
            font=("Segoe UI", 36, "bold"),
            fill="white"
        )

        # load icons

        self.student_icon = ImageTk.PhotoImage(
            Image.open("images/student.png").resize((150, 150), Image.LANCZOS)
        )

        self.face_icon = ImageTk.PhotoImage(
            Image.open("images/face.png").resize((150, 150), Image.LANCZOS)
        )

        self.attendance_icon = ImageTk.PhotoImage(
            Image.open("images/attendance.png").resize((150, 150), Image.LANCZOS)
        )

        self.train_icon = ImageTk.PhotoImage(
            Image.open("images/train.png").resize((150, 150), Image.LANCZOS)
        )

        self.photos_icon = ImageTk.PhotoImage(
            Image.open("images/photos.png").resize((150, 150), Image.LANCZOS)
        )

        self.developer_icon = ImageTk.PhotoImage(
            Image.open("images/developer.png").resize((150, 150), Image.LANCZOS)
        )

        # round rectangle function

        def round_rectangle(x1, y1, x2, y2, radius=35, **kwargs):

            points = [
                x1 + radius, y1,
                x2 - radius, y1,
                x2, y1,
                x2, y1 + radius,
                x2, y2 - radius,
                x2, y2,
                x2 - radius, y2,
                x1 + radius, y2,
                x1, y2,
                x1, y2 - radius,
                x1, y1 + radius,
                x1, y1
            ]

            return self.canvas.create_polygon(points, smooth=True, **kwargs)

        # student button

        student_border = round_rectangle(
            300 - 120, 240 - 100,
            300 + 120, 240 + 100,
            radius=35,
            outline="white",
            width=3,
            fill=""
        )

        student_btn = tk.Button(
            root,
            image=self.student_icon,
            bg="black",
            borderwidth=0,
            cursor="hand2",
            command=self.student_details
        )

        self.canvas.create_window(300, 240, window=student_btn)

        student_btn.bind("<Enter>", lambda e: self.canvas.itemconfig(student_border, width=6))
        student_btn.bind("<Leave>", lambda e: self.canvas.itemconfig(student_border, width=3))

        # face button

        face_border = round_rectangle(
            750 - 120, 240 - 100,
            750 + 120, 240 + 100,
            radius=35,
            outline="white",
            width=3,
            fill=""
        )

        face_btn = tk.Button(root, image=self.face_icon, bg="black", command=self.face_data, borderwidth=0, cursor="hand2")

        self.canvas.create_window(750, 240, window=face_btn)

        face_btn.bind("<Enter>", lambda e: self.canvas.itemconfig(face_border, width=6))
        face_btn.bind("<Leave>", lambda e: self.canvas.itemconfig(face_border, width=3))

        # attendance button

        attendance_border = round_rectangle(
            1200 - 120, 240 - 100,
            1200 + 120, 240 + 100,
            radius=35,
            outline="white",
            width=3,
            fill=""
        )

        attendance_btn = tk.Button(root, image=self.attendance_icon, bg="black", borderwidth=0, cursor="hand2")

        self.canvas.create_window(1200, 240, window=attendance_btn)

        attendance_btn.bind("<Enter>", lambda e: self.canvas.itemconfig(attendance_border, width=6))
        attendance_btn.bind("<Leave>", lambda e: self.canvas.itemconfig(attendance_border, width=3))

        # train button

        train_border = round_rectangle(
            300 - 120, 480 - 100,
            300 + 120, 480 + 100,
            radius=35,
            outline="white",
            width=3,
            fill=""
        )

        train_btn = tk.Button(root, image=self.train_icon, command=self.train_data, bg="black", borderwidth=0, cursor="hand2")

        self.canvas.create_window(300, 480, window=train_btn)

        train_btn.bind("<Enter>", lambda e: self.canvas.itemconfig(train_border, width=6))
        train_btn.bind("<Leave>", lambda e: self.canvas.itemconfig(train_border, width=3))

        # ================= PHOTOS BUTTON =================

        photos_border = round_rectangle(
            750 - 120, 480 - 100,
            750 + 120, 480 + 100,
            radius=35,
            outline="white",
            width=3,
            fill=""
        )

        photos_btn = tk.Button(root, image=self.photos_icon, command=self.open_img, bg="black", borderwidth=0, cursor="hand2")

        self.canvas.create_window(750, 480, window=photos_btn)

        photos_btn.bind("<Enter>", lambda e: self.canvas.itemconfig(photos_border, width=6))
        photos_btn.bind("<Leave>", lambda e: self.canvas.itemconfig(photos_border, width=3))

        # ================= DEVELOPER BUTTON =================

        developer_border = round_rectangle(
            1200 - 120, 480 - 100,
            1200 + 120, 480 + 100,
            radius=35,
            outline="white",
            width=3,
            fill=""
        )

        developer_btn = tk.Button(root, image=self.developer_icon, bg="black", borderwidth=0, cursor="hand2")

        self.canvas.create_window(1200, 480, window=developer_btn)

        developer_btn.bind("<Enter>", lambda e: self.canvas.itemconfig(developer_border, width=6))
        developer_btn.bind("<Leave>", lambda e: self.canvas.itemconfig(developer_border, width=3))

        # ================= HELP & EXIT =================

        help_btn = tk.Button(
            root,
            text="Help Desk",
            font=("Segoe UI", 14, "bold"),
            bg="#ff3b3b",
            fg="white",
            relief="flat",
            padx=22,
            pady=8,
            cursor="hand2"
        )

        exit_btn = tk.Button(
            root,
            text="Exit",
            font=("Segoe UI", 14, "bold"),
            bg="#ff3b3b",
            fg="white",
            relief="flat",
            padx=22,
            pady=8,
            cursor="hand2",
            command=self.exit_system
        )

        self.canvas.create_window(680, 650, window=help_btn)
        self.canvas.create_window(820, 650, window=exit_btn)

    # ================= EXIT SYSTEM =================

    def exit_system(self):

        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()
    

    def open_img(self):
        os.startfile("data")


    # function buttons

    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def train_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

    def face_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)




# ================= MAIN =================

if __name__ == "__main__":

    root = tk.Tk()
    app = FaceRecognitionUI(root)
    root.mainloop()