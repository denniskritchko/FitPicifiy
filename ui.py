import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk
import cv2
import os
import subprocess
import glob

def select_image():
    file_path = filedialog.askopenfilename(filetypes= [("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        input_label.config(text=f"Selected: {os.path.basename(file_path)}")
        display_image(file_path, original_image_label)
        process_and_display_image(file_path)

def process_and_display_image(image_path):
    outputs_folder = "outputs"
    if not os.path.exists(outputs_folder):
        os.makedirs(outputs_folder)

    base_output_path = os.path.join(outputs_folder, "output.jpg")
    subprocess.run(["python", "fitpicify.py", image_path, base_output_path])

    output_files = sorted(glob.glob(os.path.join(outputs_folder, "output*.jpg")), key = os.path.getctime)
    latest_output = output_files[-1] if output_files else None

    if latest_output:
        display_image(latest_output, edited_image_label)

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