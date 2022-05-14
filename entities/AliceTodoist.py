import json
import logging
from todoist_api_python.api import TodoistAPI
from additionalfunction.TimeHelper import DateSettings, DayMonth, FromToDateTime, addZ, getDateForFilter, getTime, getTimeDatetime, minusDaysDate, plusDaysDate, plusDaysDatetime, todayDate, todayDatetime
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

    def get_list_task_name_by_project_and_time(self, project_name = None, dayMonthTime = None):
        listTask = []
        if project_name:
            got_project_id = self.get_project_id_by_name(project_name)
            if(got_project_id):
                listTask = self.todoist.get_tasks(project_id = got_project_id, filter = getDateForFilter(dayMonthCount=dayMonthTime))
            else:
                return Tasks("У вас нет такого проекта. Создать проект?", -1)
        else:
            if dayMonthTime:
                listTask = self.todoist.get_tasks(filter = getDateForFilter(dayMonthCount=dayMonthTime))
            else:
                listTask = self.todoist.get_tasks(filter = getDateForFilter(dayMonthCount=DayMonth(day=0)))

        return build_task_entity(listTask)

    def get_overdue_tasks_with_project(self, project_name = None):
        listTask = []
        if project_name:
            got_project_id = self.get_project_id_by_name(project_name)
            if(got_project_id):
                today = todayDate() #minusDaysDate(1)
                listTask = self.todoist.get_tasks(project_id = got_project_id, filter=f"due before: {today}")
        else:
            listTask = self.todoist.get_tasks(filter = "overdue")

        return listTask
    
    def get_list_overdue_task(self, project_name = None):
        listTask = self.get_overdue_tasks_with_project(project_name)

        if listTask == []: 
            return Tasks("У вас нет такого проекта. Создать проект?", -1)
        else:
            return build_task_entity(listTask)

    def get_list_non_or_recurring_task(self, project_name = None, non_reccuring = None):
        listTask = []
        filter = "recurring"
        if non_reccuring:
            yesterday = minusDaysDate(1)
            filter = f"due after: {yesterday} & !recurring"
        
        if project_name:
            got_project_id = self.get_project_id_by_name(project_name)
            if(got_project_id):
                listTask = self.todoist.get_tasks(project_id = got_project_id, filter = filter)
            else:
                return Tasks("У вас нет такого проекта. Создать проект?", -1)
        else:
            listTask = self.todoist.get_tasks(filter = filter)

        return build_task_entity(listTask)

    def get_list_task_coming_hours_by_project_name(self, project_name = None, hours = None):
        listTask = []
        if project_name:
            got_project_id = self.get_project_id_by_name(project_name)
            if(got_project_id):
                listTask = self.todoist.get_tasks(project_id = got_project_id, filter = f"due before: +{hours} hours & !overdue")
            else:
                return Tasks("У вас нет такого проекта. Создать проект?", -1)
        else:
            if hours:
                listTask = self.todoist.get_tasks(filter = f"due before: +{hours} hours & !overdue")
            else:
                listTask = self.todoist.get_tasks(filter = getDateForFilter(dayMonthCount=DayMonth(day=0)))

        return build_task_entity(listTask)

    def get_list_tasks(self, filter = None, project_id = None):
        return self.todoist.get_tasks(project_id = project_id, filter = filter)

    def reschedule_tasks(self, project_name = None, dayMonthTime = DayMonth(day=0)):
        listTask = self.get_overdue_tasks_with_project(project_name)

        proc = Thread(target = self.update_task, args = (listTask, dayMonthTime,))
        proc.start()

        if listTask == []: 
            return Tasks("У вас нет такого проекта. Создать проект?", -1)
        else:
            return build_task_entity(listTask)

    def update_task(self, tasks: list[Task], dayMonth: DayMonth):
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
                if dayMonth.month:
                    date = todayDatetime(date, task.due.timezone, dayMonth=dayMonth)
                else:    
                    if dayMonth.day == 0:
                        date = todayDatetime(date, task.due.timezone)
                    else:
                        date = plusDaysDatetime(date, dayMonth.day, task.due.timezone)
            else: 
                date = task.due.date
                if dayMonth.month:
                    date = todayDate(dayMonth)
                else:
                    if dayMonth == 0:
                        date = todayDate()
                    else:
                        date = plusDaysDate(date, dayMonth.day)
            
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
    
    def add_tasks(self, project_name: str, content_tasks: list[str], dateSettings: DateSettings):
        project_id = None
        if project_name:
            got_project_id = self.get_project_id_by_name(project_name)
            if(got_project_id):
                project_id = got_project_id
            else:
                return Tasks("У вас нет такого проекта. Создать проект?", -1)

        proc = Thread(target = self.add_task, args = (project_id, content_tasks, dateSettings,))
        proc.start()

        return Tasks("Отлично, задача добавлена. Добавим ещё что-нибудь?", 1)
        
    def add_task(self, project_id: str, content_tasks: list[str], dateSettings: DateSettings):
        token = self.todoist._token
        headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        commands = []
        date = dateSettings.datetime
        if not date:
            date = dateSettings.date
            if date:
                date = date.isoformat()
        else:
            date = date.isoformat()
        logging.info(f"date - {date}")
        for content_task in content_tasks:
            commands.append({
                    "type": "item_add", 
                    "temp_id": str(uuid.uuid4()),
                    "uuid": str(uuid.uuid4()),
                    "args": {
                        "content": content_task, 
                        "project_id": project_id,
                        "due": {
                            "date": date,
                            "timezone": dateSettings.timezone,
                            "lang": "en",
                            "is_recurring": dateSettings.recurring,
                        },
                    }
                })
        
        data = 'commands=' + json.dumps(commands)
        requests.post('https://api.todoist.com/sync/v8/sync', headers=headers, data=data)