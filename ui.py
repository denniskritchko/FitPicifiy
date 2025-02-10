import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk, ExifTags
import cv2
import os
import subprocess
import glob


"""allows the user to select an image file from the file dialog"""
def select_image():
    file_path = filedialog.askopenfilename(filetypes= [("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        input_label.config(text=f"Selected: {os.path.basename(file_path)}")
        display_image(file_path, input_label)
        process_and_display_image(file_path)

""""processes the image from fitpicify.py and displays the output image"""
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

"""displays the image on the label"""
def display_image(image_path, label):
    image = Image.open(image_path)

    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())
        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass

    image.thumbnail((300, 300))
    img = ImageTk.PhotoImage(image)
    label.config(image=img)
    label.image = img

"""creates the main window and widgets"""
root = tk.Tk()
root.title("Fitpicify")
root.geometry("640x480")
root.configure(background="gray")


select_button = Button(root, text="Select Image to Edit", command=select_image, bg="light blue", fg="black")
select_button.pack()

input_label = Label(root)
input_label.pack(side="left", padx=10, pady=10)

edited_image_label = Label(root)
edited_image_label.pack(side="right", padx=10, pady=10)

"""starts the main event loop"""
root.mainloop()