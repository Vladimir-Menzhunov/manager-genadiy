from todoist_api_python.api import TodoistAPI

from entities.AliceRequest import AliceRequest

class AliceTodoist:
    """Класс AliceTodoist предназначен для реализации удобного интерфейса взаимодействия
    с Todoist.
    -------------------------------------------------------------------------------------
    Задача класса - предоставлять удобный доступ к компонентам ответа Todoist и отдавать ответ в навык.
    -------------------------------------------------------------------------------------
    Методы
        get_list_project_name - получение имён проекта
    """

    def __init__(self, request: AliceRequest):
        """Конструктор класса принимает аргумента класса AliceRequest для установки access_token
        для ответа."""
        self.todoist = TodoistAPI(request.access_token)

    def get_list_project_name(self):
        projects = self.todoist.get_projects()
        projects_names = ""
        count = 1
        for project in projects:
            projects_names += "{} - {}\n".format(count, project.name)
            count += 1
        return projects_names

