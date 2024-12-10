import os
import customtkinter as ctk
from tkinter import messagebox
import requests
import logging

# Directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Configure logging
logging.basicConfig(filename=os.path.join(SCRIPT_DIR, 'upload_log.txt'), level=logging.INFO, 
                    format='%(asctime)s %(message)s')

# Wigle API credentials
WIGLE_API_URL = 'https://api.wigle.net/api/v2/file/upload'
WIGLE_API_USER = 'YOUR WIGLE API Name HERE'
WIGLE_API_TOKEN = 'YOUR WIGLE API Token HERE'

# SD card directory to monitor for new files (e.g., 'G:\\')
WATCH_DIRECTORY = 'YOUR SD CARD DRIVE PATH HERE'

# File to keep track of uploaded files
UPLOADED_FILES_TRACKER = os.path.join(SCRIPT_DIR, 'uploaded_files.txt')

def get_uploaded_files():
    if not os.path.exists(UPLOADED_FILES_TRACKER):
        return set()
    with open(UPLOADED_FILES_TRACKER, 'r') as f:
        return set(line.strip() for line in f)

def save_uploaded_file(filename):
    with open(UPLOADED_FILES_TRACKER, 'a') as f:
        f.write(f'{filename}\n')

def list_new_files(directory, uploaded_files):
    return [f for f in os.listdir(directory) if f.endswith('.log') and f not in uploaded_files]

def upload_file(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(WIGLE_API_URL, auth=(WIGLE_API_USER, WIGLE_API_TOKEN), files=files)
        logging.info(f"Uploading {file_path}: {response.status_code} - {response.text}")
        return response.status_code == 200, response.text

class ScrollableCheckBoxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for item in item_list:
            self.add_item(item)

    def add_item(self, item):
        frame = ctk.CTkFrame(self)
        frame.grid_columnconfigure(0, weight=1)
        checkbox = ctk.CTkCheckBox(frame, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=0, column=0, sticky="w")
        frame.grid(row=len(self.checkbox_list), column=0, pady=(0, 10), sticky="w")
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]

def select_files():
    uploaded_files = get_uploaded_files()
    new_files = list_new_files(WATCH_DIRECTORY, uploaded_files)
    
    def upload_selected_files():
        selected_files = scrollable_checkbox_frame.get_checked_items()
        if not selected_files:
            messagebox.showwarning("No Selection", "No files selected for upload.")
            return
        
        all_success = True
        for file_name in selected_files:
            file_path = os.path.join(WATCH_DIRECTORY, file_name)
            success, response_text = upload_file(file_path)
            if success:
                save_uploaded_file(file_name)
            else:
                all_success = False
                messagebox.showerror("Error", f"Failed to upload {file_name}. Response: {response_text}")
        
        if all_success:
            messagebox.showinfo("Success", "All selected files uploaded successfully.")
            root.destroy()  # Close the GUI

    # Create a GUI window
    ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("green")  # Themes: "blue" (default), "green", "dark-blue"

    root = ctk.CTk()
    root.title("Wigle File Uploader")
    root.geometry("270x500")
    root.attributes('-topmost', True)  # Keep the window on top

    # Set the window icon
    icon_path = os.path.join(SCRIPT_DIR, 'icon.ico')  # Path to your icon image
    root.iconbitmap(icon_path)
    
    title_label = ctk.CTkLabel(root, text="Select Files to Upload", font=("Arial", 20))
    title_label.pack(pady=20)

    scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=root, width=230, height=300, item_list=new_files)
    scrollable_checkbox_frame.pack(pady=0, padx=20, fill="both", expand=True)

    upload_button = ctk.CTkButton(root, text="Upload Selected Files", command=upload_selected_files, font=("Arial", 20), width=230, height=50)
    upload_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    select_files()
