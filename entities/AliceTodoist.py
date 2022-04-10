import logging
from todoist_api_python.api import TodoistAPI
from additionalfunction.compatefunc import cosine_compare
import operator
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
        
        projectid_cosine_dict = {project.id : cosine_compare(project.name, project_name) for project in projects}
        
        project_cosine = max(projectid_cosine_dict.items(), key=operator.itemgetter(1))
        
        logging.info(f"cosine: {project_cosine[1]}, projectTodoist: {project_cosine[0]}, projectGot: {project_name}")
        if(project_cosine[1] < 0.7):
            return None

        logging.info(f"project_id: {project_cosine[0]}")
        return project_cosine[0]
        

    def get_list_task_name_by_project_and_time(self, project_name = None, time = None):
        listTask = []
        if project_name and time:
            print("project time")
        elif project_name:
            got_project_id = self.get_project_id_by_name(project_name)
            if(got_project_id):
                listTask = self.todoist.get_tasks(project_id = got_project_id)
            else:
                return Tasks("У вас нет такого проекта. Создать проект?", -1)
        elif time: 
            print("time")
        else:
            listTask = self.todoist.get_tasks(filter = "today")

        tasks_names = ""
        count = 0
        if(listTask):
            count = 1
            for task in listTask:
                content = ""
                if(len(task.content) > 20):
                    content = f"{task.content[:20]}..."
                else:
                    content = task.content

                tasks_names += "{} - {}\n".format(count, content)
                count += 1
        else:
            tasks_names = "Задач нет!"
        return Tasks(tasks_names, count)

