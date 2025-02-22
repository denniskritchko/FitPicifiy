import cv2
import numpy as np
from PIL import Image, ImageEnhance
import argparse
import os

"""adjusts exposure using a lookup table and a power function by the factor of 1.3"""
def adjust_exposure(image, factor = 1.3):
    table = np.array([(i / 255.0) ** factor * 255 for i in range(256)]).astype("uint8")
    return cv2.LUT(image, table)

"""adjusts brightness using the ImageEnhance module by the factor of 0.7"""
def adjust_brightness(image, factor=0.7):
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Brightness(pil_image)
    enhanced = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(enhanced), cv2.COLOR_RGB2BGR)

"""dynamically adjusts temperature over the kelvin table by default kelvin of 6500"""
def adjust_temperature(image, kelvin=6500):
    kelvin_table = {
        1000: (255, 56, 0), 2000: (255, 138, 18), 3000: (255, 180, 107),
        4000: (255, 209, 163), 5000: (255, 228, 206), 6500: (255, 249, 253),
        7500: (245, 243, 255), 10000: (235, 235, 255)
    }
    r, g, b = kelvin_table.get(kelvin, kelvin_table[6500])
    balance = np.array([b / 255.0, g / 255.0, r / 255.0])
    return np.clip(image * balance, 0, 255).astype(np.uint8)

"""adjusts contrast using the ImageEnhance module by the factor of 1.5"""
def adjust_contrast(image, factor=1.5):
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Contrast(pil_image)
    enhanced = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(enhanced), cv2.COLOR_RGB2BGR)

"""gets a unique filename by appending a counter to the base filename"""
def get_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filename):
        filename = f"{base}_{counter}{ext}"
        counter += 1
    return filename

"""processes the image by adjusting exposure, brightness, temperature, and contrast"""
def process_image(image_path, output_path):

    outputs_folder = "outputs"
    if not os.path.exists(outputs_folder):
        os.makedirs(outputs_folder)

    output_path = os.path.join(outputs_folder, os.path.basename(output_path))
    output_path = get_unique_filename(output_path)

    image = cv2.imread(image_path)
    image = adjust_exposure(image)
    image = adjust_brightness(image, factor=0.9)
    image = adjust_temperature(image, kelvin=5000)
    image = adjust_contrast(image, factor=1.0)
    cv2.imwrite(output_path, image)

"""parse the input arguments and process the image"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto-adjust image exposure, temperature, and contrast.")
    parser.add_argument("input", help="inputs/<your_image_here>.jpg")
    parser.add_argument("output", help="outputs/output.jpg")
    args = parser.parse_args()
    process_image(args.input, args.output)
