import tkinter as tk
from PIL import Image

root = tk.Tk()

# Create Canvas
canvas = tk.Canvas(root, width=600, height=800)
canvas.grid(columnspan=3)

# Create Logo
# logo = Image.open("logo.svg")
# logo = ImageTk.PhotoImage(logo)
# logo_label = tk.Label(image=logo)
# logo_label.image = logo
# logo_label.grid(column=1, row=0)


root.mainloop()