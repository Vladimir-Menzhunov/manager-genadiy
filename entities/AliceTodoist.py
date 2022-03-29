from todoist_api_python.api import TodoistAPI

from entities.AliceRequest import AliceRequest

class Projects:
    def __init__(self, projects, len):
        self.projects = projects
        self.len = len

class Tasks:
    def __init__(self, tasks, len):
        self.tasks = tasks
        self.len = len

class AliceTodoist:
    """Класс AliceTodoist предназначен для реализации удобного интерфейса взаимодействия
    с Todoist.
    -------------------------------------------------------------------------------------
    Задача класса - предоставлять удобный доступ к компонентам ответа Todoist и отдавать ответ в навык.
    -------------------------------------------------------------------------------------
    Методы
        get_list_project_name - получение проектов в виде строки и длинны
    """

    def __init__(self, request: AliceRequest):
        """Конструктор класса принимает аргумента класса AliceRequest для установки access_token
        для ответа."""
        self.todoist = TodoistAPI(request.access_token)

    def get_list_project_name(self) -> Projects:
        projects = self.todoist.get_projects()
        projects_names = ""
        count = 1
        for project in projects:
            projects_names += "{} - {}\n".format(count, project.name)
            count += 1
        return Projects(projects_names, count)

    def get_list_task_name_by_project_and_time(self, project = None, time = None):
        listTask = []
        if project and time:
            print("project time")
        elif project:
            print("project")
        elif time: 
            print("time")
        else:
            listTask = self.todoist.get_tasks(filter = "today")

        tasks_names = ""
        count = 1
        for task in listTask:
            tasks_names += "{} - {}\n".format(count, task.content)
            count += 1
        return Tasks(tasks_names, count)

