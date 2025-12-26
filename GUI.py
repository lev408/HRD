import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def star_data(name_star, temperature, magnitude, spectrum_raw_path, spectrum_path):
    print(spectrum_path)
    print(spectrum_raw_path)
    root = tk.Toplevel()

    root.geometry("400x400")

    name = ttk.Label(root, text=f"name: {name_star}")
    magnitude = ttk.Label(root, text=f"magnitude: {magnitude}mag")
    temperature = ttk.Label(root, text=f"temperature: {temperature}K")
    root.title(str(name_star))

    name.pack(side="top", anchor="nw")
    magnitude.pack(side="top", anchor="nw")
    temperature.pack(side="top", anchor="nw")

    image_spectrum = Image.open(spectrum_path)
    photo_spectrum = ImageTk.PhotoImage(image_spectrum)
    label_spectrum = ttk.Label(root, text="ausgewertetes Spektrum", image=photo_spectrum, compound="bottom",
                               padding=5)

    image_spectrum_raw = Image.open(spectrum_raw_path)
    photo_spectrum_raw = ImageTk.PhotoImage(image_spectrum_raw)
    label_spectrum_raw = ttk.Label(root, text="Emissionsspektrum", image=photo_spectrum_raw, compound="bottom",
                                   padding=5)

    label_spectrum_raw.pack(side="top", anchor="nw")
    label_spectrum.pack(side="top", anchor="nw")

    root.mainloop()
