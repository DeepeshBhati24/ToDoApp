# backend.py
import json


class ToDoBackend:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []  # Return an empty list if the file doesn't exist

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, task):
        self.tasks.append({"task": task, "tags": [], "reminder": None})
        self.save_tasks()

    def delete_task(self, index):
        del self.tasks[index]
        self.save_tasks()

    def modify_task(self, index, new_task):
        self.tasks[index]["task"] = new_task
        self.save_tasks()

    def tag_member(self, index, member):
        if member not in self.tasks[index]["tags"]:
            self.tasks[index]["tags"].append(member)
            self.save_tasks()

    def set_reminder(self, index, reminder_time):
        self.tasks[index]["reminder"] = reminder_time
        self.save_tasks()
