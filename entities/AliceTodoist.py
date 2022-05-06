import json
import logging
from todoist_api_python.api import TodoistAPI
from additionalfunction.TimeHelper import getTime, getTimeDatetime, plusDaysDate, plusDaysDatetime, todayDate, todayDatetime
from additionalfunction.comparefunc import cosine_compare
import operator
from constants import LENGTH_CONTENT, LENGTH_TEXT
from entities.AliceRequest import AliceRequest
import requests
from todoist_api_python.models import Task
import uuid
from threading import Thread

class Projects:
    def __init__(self, projects, len):
        self.projects = projects
        self.len = len

class Tasks:
    def __init__(self, tasks, len):
        self.tasks = tasks
        self.len = len

def sort_key(t: Task):
    time = getTime(t.due)
    return time.timestamp()

def build_task_entity(task_list: list[Task]):
    count = 0
    tasks_names = ""
    if(task_list):
        task_list = sorted(task_list, key=sort_key)
        for task in task_list:
            content = ""
            
            if(len(task.content) > LENGTH_CONTENT):
                content = f"{task.content[:LENGTH_CONTENT]}..."
            else:
                content = task.content

            if task.due:
                content += f"{getTimeDatetime(task.due)}"

            count += 1
            tasks_names += "{} - {}\n".format(count, content)
    else:
        tasks_names = "Задач нет!"

    if(len(tasks_names) > LENGTH_TEXT):
        tasks_names = f"{tasks_names[:LENGTH_TEXT]}..."
    
    return Tasks(tasks_names, count)

class AliceTodoist:
    """Класс AliceTodoist предназначен для реализации удобного интерфейса взаимодействия
    с Todoist.
    -------------------------------------------------------------------------------------
    Задача класса - предоставлять удобный доступ к компонентам ответа Todoist и отдавать ответ в навык.
    -------------------------------------------------------------------------------------
    Методы
        get_list_project_name - получение проектов в виде строки и длинны
        get_project_id_by_name - получение id проекта по имени
        get_list_task_name_by_project_and_time - получение задач по проекту и времени
        reschedule_tasks - перенос задач по проекту и времени
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
        if(project_cosine[1] < 0.72):
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

        return build_task_entity(listTask)
    
    def get_list_tasks(self, filter = None):
        return self.todoist.get_tasks(filter = filter)

    def reschedule_tasks(self, project_name = None, dayTime = 0):
        listTask = []
        if project_name:
            got_project_id = self.get_project_id_by_name(project_name)
            if(got_project_id):
                listTask = self.todoist.get_tasks(project_id = got_project_id, filter="overdue")
            else:
                return Tasks("У вас нет такого проекта. Создать проект?", -1)
        else:
            listTask = self.todoist.get_tasks(filter = "overdue")

        proc = Thread(target = self.update_task, args = (listTask, dayTime,))
        proc.start()

        return build_task_entity(listTask)

    def update_task(self, tasks: list[Task], timeCount):
        token = self.todoist._token
        headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        commands = []

        for task in tasks:
            #logging.info(f"task.id - {task.id}, task.due.datetime - {task.due.datetime}, task.due.date - {task.due.date}")
            date = task.due.datetime
            if date:
                if timeCount == 0:
                    date = todayDatetime(date, task.due.timezone)
                else:
                    date = plusDaysDatetime(date, timeCount, task.due.timezone)
            else: 
                date = task.due.date
                if timeCount == 0:
                    date = todayDate(date)
                else:
                    date = plusDaysDate(date, timeCount)
            
            commands.append({
                    "type": "item_update", 
                    "uuid": str(uuid.uuid4()),
                    "args": {
                        "id": task.id, 
                        "due": {
                            "date": date,
                            "timezone": 'Europe/Moscow',
                            "string": task.due.string,
                            "lang": "en",
                            "is_recurring": task.due.recurring,
                        },
                    }
                })
        
        data = 'commands=' + json.dumps(commands)
        requests.post('https://api.todoist.com/sync/v8/sync', headers=headers, data=data)
        