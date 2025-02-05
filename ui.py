import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk
import cv2
import os
import subprocess

def select_image():
    file_path = filedialog.askopenfilename(filetypes= [("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        input_label.config(text=f"Selected: {os.path.basename(file_path)}")
        display_image(file_path, original_image_label)
        process_and_display_image(file_path)

def process_and_display_image(image_path):
    output_path = "output.jpg"
    subprocess.run(["python", "fitpicify.py", image_path, output_path])
    display_image(output_path, edited_image_label)

def display_image(image_path, label):
    image = Image.open(image_path)
    image.thumbnail((300, 300))
    img = ImageTk.PhotoImage(image)
    label.config(image=img)
    label.image = img

root = tk.Tk()
root.title("Fitpicify")

input_label = Label(root, text="Select an image")
input_label.pack()

select_button = Button(root, text="Select Image", command=select_image)
select_button.pack()

original_image_label = Label(root)
original_image_label.pack()

edited_image_label = Label(root)
edited_image_label.pack()

root.mainloop()