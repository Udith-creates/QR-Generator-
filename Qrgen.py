import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageTk
import qrcode
import io
import os

# Global variables
qr_color = "black"
bg_color = "white"
logo_path = None
final_qr_image = None

# Generate the QR Code
def generate_qr():
    global final_qr_image

    url = entry.get().strip()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL.")
        return

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=qr_color, back_color=bg_color).convert("RGB")

    # Add logo
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path)
        logo = logo.resize((80, 80))
        pos = ((img.size[0] - 80) // 2, (img.size[1] - 80) // 2)
        img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

    final_qr_image = img

    # Display in GUI
    img_resized = img.resize((200, 200))
    tk_img = ImageTk.PhotoImage(img_resized)
    qr_label.config(image=tk_img)
    qr_label.image = tk_img
    save_button.config(state="normal")

# Save QR Code
def save_qr():
    if final_qr_image:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Files", "*.png")])
        if file_path:
            final_qr_image.save(file_path)
            messagebox.showinfo("Success", "QR code saved!")

# Choose QR and BG Colors
def choose_qr_color():
    global qr_color
    color = colorchooser.askcolor(title="Choose QR Color")
    if color[1]:
        qr_color = color[1]

def choose_bg_color():
    global bg_color
    color = colorchooser.askcolor(title="Choose Background Color")
    if color[1]:
        bg_color = color[1]

# Choose Logo
def choose_logo():
    global logo_path
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if path:
        logo_path = path
        messagebox.showinfo("Logo Selected", f"Logo set:\n{path}")

# UI Setup
root = tk.Tk()
root.title("🎨 Stylish QR Code Generator")
root.geometry("420x550")
root.configure(bg="#f2f4f8")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 11), background="#f2f4f8")

# Title
ttk.Label(root, text="🔗 Enter Portfolio URL:", font=("Segoe UI", 12, "bold")).pack(pady=10)

# URL Entry
entry = ttk.Entry(root, width=45)
entry.pack(pady=5)

# Button Frame
btn_frame = tk.Frame(root, bg="#f2f4f8")
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="🎨 Pick QR Color", command=choose_qr_color).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(btn_frame, text="🌈 Pick BG Color", command=choose_bg_color).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(btn_frame, text="🖼️ Add Logo", command=choose_logo).grid(row=0, column=2, padx=5, pady=5)

# Generate Button
ttk.Button(root, text="🚀 Generate QR Code", command=generate_qr).pack(pady=10)

# QR Display
qr_label = tk.Label(root, bg="#f2f4f8")
qr_label.pack(pady=10)

# Save Button
save_button = ttk.Button(root, text="💾 Save QR Code", command=save_qr, state="disabled")
save_button.pack(pady=10)

# Footer
ttk.Label(root, text="QR GENERATOR BY UDITH <3", font=("Segoe UI", 9)).pack(pady=5)

root.mainloop()
