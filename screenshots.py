import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
import time
import os

class ScreenCaptureApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Screen Capture Tool")
        self.master.geometry("400x300")
        
        self.output_directory = os.getcwd()
        self.base_name = "capture"
        self.image_format = ".png"
        self.timer = 5
        
        self.build_interface()
    
    def build_interface(self):
        tk.Label(self.master, text="Screen Capture Tool", font=("Arial", 16)).pack(pady=10)

        # Timer input
        tk.Label(self.master, text="Capture Delay (seconds):").pack(pady=5)
        self.timer_input = tk.Entry(self.master)
        self.timer_input.insert(0, str(self.timer))
        self.timer_input.pack()

        # File name input
        tk.Label(self.master, text="File Name:").pack(pady=5)
        self.name_input = tk.Entry(self.master)
        self.name_input.insert(0, self.base_name)
        self.name_input.pack()

        # File format dropdown
        tk.Label(self.master, text="Image Format:").pack(pady=5)
        self.format_option = tk.StringVar(value=self.image_format)
        tk.OptionMenu(self.master, self.format_option, ".png", ".jpeg", ".bmp").pack()

        # Directory selection
        tk.Label(self.master, text="Save Directory:").pack(pady=5)
        self.directory_label = tk.Label(self.master, text=self.output_directory, fg="blue")
        self.directory_label.pack()
        tk.Button(self.master, text="Choose Folder", command=self.select_directory).pack(pady=5)

        # Action buttons
        tk.Button(self.master, text="Capture Full Screen", command=self.full_screen_capture).pack(pady=5)
        tk.Button(self.master, text="Capture Selected Area", command=self.region_capture).pack(pady=5)
    
    def select_directory(self):
        folder = filedialog.askdirectory(initialdir=self.output_directory, title="Choose Save Location")
        if folder:
            self.output_directory = folder
            self.directory_label.config(text=self.output_directory)

    def full_screen_capture(self):
        self.set_timer()
        time.sleep(self.timer)
        snapshot = pyautogui.screenshot()
        self.save_image(snapshot)

    def region_capture(self):
        self.set_timer()
        time.sleep(self.timer)
        messagebox.showinfo("Info", "Drag and select the area for capturing. Press Enter to confirm.")

        region = pyautogui.screenshot()  
        selected_region = pyautogui.selectRegion()
        
        if selected_region:
            x, y, width, height = selected_region
            snapshot = pyautogui.screenshot(region=(x, y, width, height))
            self.save_image(snapshot)
        else:
            messagebox.showerror("Error", "Region selection failed. Try again.")

    def set_timer(self):
        try:
            self.timer = int(self.timer_input.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid delay! Defaulting to 5 seconds.")
            self.timer = 5

    def save_image(self, snapshot):
        file_name = self.name_input.get() or "capture"
        file_ext = self.format_option.get()
        file_path = os.path.join(self.output_directory, file_name + file_ext)
        try:
            snapshot.save(file_path)
            messagebox.showinfo("Success", f"Image saved at {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save image: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenCaptureApp(root)
    root.mainloop()