# app.py
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
from service import ToDoService
from backend import ToDoBackend
from PIL import Image, ImageTk  # Import Pillow to handle images


class ToDoApp:
    def __init__(self, root, service):
        self.root = root
        self.service = service
        self.root.title("To-Do List App")
        self.root.geometry("500x500")  # Adjusted to fit the image and listbox

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10)

        # Add an image (e.g., logo.png) at the top
        self.add_image()

        self.task_listbox = tk.Listbox(self.main_frame, width=50, height=10)  # Adjusted height
        self.task_listbox.grid(row=1, column=0, padx=10, pady=10)

        self.load_task_list()

        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=5)

        self.menu_button = ttk.Menubutton(self.menu_frame, text="Options")
        self.menu_button.grid(row=0, column=0, padx=5)

        self.menu = tk.Menu(self.menu_button, tearoff=0)
        self.menu.add_command(label="Add Task", command=self.add_task)
        self.menu.add_command(label="Delete Task", command=self.delete_task)
        self.menu.add_command(label="Modify Task", command=self.modify_task)
        self.menu.add_command(label="Tag Member", command=self.tag_member)
        self.menu.add_command(label="Set Reminder", command=self.set_reminder)
        self.menu_button.config(menu=self.menu)

    def add_image(self):
        # Load and display the image at the top of the window
        try:
            # Open the image using Pillow
            image = Image.open("logo.png")  # Adjust the path as needed
            image = image.resize((150, 150))  # Resize the image if needed
            photo = ImageTk.PhotoImage(image)  # Convert to a format tkinter can use

            # Add the image to the window using a Label widget
            self.image_label = tk.Label(self.root, image=photo)
            self.image_label.image = photo  # Keep a reference to the image object
            self.image_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    def load_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.service.get_tasks():
            self.task_listbox.insert(tk.END, task["task"])

    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter task:")
        if task:
            self.service.add_task(task)
            self.load_task_list()

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            self.service.delete_task(selected[0])
            self.load_task_list()
        else:
            messagebox.showwarning("Warning", "Select a task to delete.")

    def modify_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            new_task = simpledialog.askstring("Modify Task", "Enter new task:")
            if new_task:
                self.service.modify_task(selected[0], new_task)
                self.load_task_list()
        else:
            messagebox.showwarning("Warning", "Select a task to modify.")

    def tag_member(self):
        selected = self.task_listbox.curselection()
        if selected:
            member = simpledialog.askstring("Tag Member", "Enter member name:")
            if member:
                self.service.tag_member(selected[0], member)
                self.load_task_list()
        else:
            messagebox.showwarning("Warning", "Select a task to tag.")

    def set_reminder(self):
        selected = self.task_listbox.curselection()
        if selected:
            reminder_time = simpledialog.askstring("Set Reminder", "Enter reminder (YYYY-MM-DD HH:MM):")
            try:
                if datetime.strptime(reminder_time, "%Y-%m-%d %H:%M") > datetime.now():
                    self.service.set_reminder(selected[0], reminder_time)
                    self.load_task_list()
                else:
                    messagebox.showerror("Error", "Reminder must be in the future.")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format.")
        else:
            messagebox.showwarning("Warning", "Select a task to set a reminder.")


if __name__ == "__main__":
    backend = ToDoBackend()
    service = ToDoService(backend)
    root = tk.Tk()
    app = ToDoApp(root, service)
    root.mainloop()
