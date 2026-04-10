from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import mysql.connector
import cv2
from time import strftime
from datetime import datetime


class Face_Recognition:

    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1500x700")
        self.root.resizable(False, False)

        bg_img = Image.open("images/bg.png").resize((1500, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(bg_img)

        self.canvas = tk.Canvas(root, width=1500, height=750, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")

        self.canvas.create_text(
            750, 60,
            text="Face Recognition",
            font=("Segoe UI", 36, "bold"),
            fill="white"
        )

        fr_img = Image.open("images/face_recognition.png").resize((1400, 510), Image.LANCZOS)
        self.fr_photo = ImageTk.PhotoImage(fr_img)

        self.canvas.create_image(750, 380, image=self.fr_photo)

        btn = tk.Button(
            root,
            text="Recognize Face",
            command=self.face_recog,
            font=("Segoe UI", 14, "bold"),
            bg="red",
            fg="white"
        )

        self.canvas.create_window(750, 560, window=btn)

    # attendance

    def mark_attendance(self,i,r,n,d):
        with open("attendance.csv","r+",newline="\n") as f:
            myDataList = f.readlines()
            name_list = []
            for line in myDataList:
                entry = line.split((",")) 
                name_list.append(entry[0])
            if((i not in name_list) and (r not in name_list) and (n not in name_list) and (d not in name_list)):
                now = datetime.now()
                d1 = now.strftime("%d/%m/%Y")
                dtString = now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{r},{n},{d},{dtString},{d1},Present")


    # ================= FACE RECOGNITION =================
    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            unknown_detected = False

            for (x, y, w, h) in features:
                id, predict = clf.predict(gray_image[y:y+h, x:x+w])
                confidence = int(100 * (1 - predict / 300))

                conn = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="bhoomi12",
                    database="face_recognizer"
                )
                my_cursor = conn.cursor()

                my_cursor.execute("SELECT student_id, name, roll, department FROM student WHERE student_id=%s", (id,))
                result = my_cursor.fetchone()

                if result:
                    i, n, r, d = result
                else:
                    i, n, r, d = "Unknown", "Unknown", "Unknown", "Unknown"

                if confidence > 77:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
                    cv2.putText(img, f"ID: {i}", (x, y-75),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Roll: {r}", (x, y-55),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Name: {n}", (x, y-30),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Department: {d}", (x, y-5),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    self.mark_attendance(i,r,n,d)
                else:
                    unknown_detected = True
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y-5),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)

            return img, unknown_detected

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        video_cap = cv2.VideoCapture(0)

        
        unknown_count = 0

        while True:
            ret, img = video_cap.read()
            if not ret:
                break

            img, unknown_detected = draw_boundary(img, faceCascade, 1.1, 10, clf)

            cv2.imshow("Welcome To Face Recognition", img)

            if unknown_detected:
                unknown_count += 1
            else:
                unknown_count = 0

            # close only after 5 unknown detections
            if unknown_count >= 5:
                cv2.waitKey(1000)
                break

            if cv2.waitKey(1) == 13:
                break
        video_cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()