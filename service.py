from backend import ToDoBackend


class ToDoService:
    def __init__(self, backend):
        self.backend = backend

    def get_tasks(self):
        return self.backend.tasks

    def add_task(self, task):
        self.backend.add_task(task)

    def delete_task(self, index):
        self.backend.delete_task(index)

    def modify_task(self, index, new_task):
        self.backend.modify_task(index, new_task)

    def tag_member(self, index, member):
        self.backend.tag_member(index, member)

    def set_reminder(self, index, reminder_time):
        self.backend.set_reminder(index, reminder_time)
