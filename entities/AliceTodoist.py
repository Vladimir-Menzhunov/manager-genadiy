import logging
from todoist_api_python.api import TodoistAPI
from additionalfunction.compatefunc import cosine_compare

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

    def get_project_id_by_name(self, project_name: str):
        projects = self.todoist.get_projects()
        
        for project in projects:
            cosine = cosine_compare(project.name, project_name)
            logging.info(f"cosine: {cosine}, projectTodoist: {project.name}, projectGot: {project_name}")
            if(cosine > 0.81):
                project_id = project.id
                logging.info(f"project_id: {project_id}")
                return project_id
        return None
        

    def get_list_task_name_by_project_and_time(self, project_name = None, time = None):
        listTask = []
        if project_name and time:
            print("project time")
        elif project_name:
            got_project_id = self.get_project_id_by_name(project_name)
            if(got_project_id):
                listTask = self.todoist.get_tasks(project_id = got_project_id)
        elif time: 
            print("time")
        else:
            listTask = self.todoist.get_tasks(filter = "today")

        tasks_names = ""
        count = 0
        if(listTask):
            count = 1
            for task in listTask:
                tasks_names += "{} - {}\n".format(count, task.content)
                count += 1
        else:
            tasks_names = "Задач нет!"
        return Tasks(tasks_names, count)

