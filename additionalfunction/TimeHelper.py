from datetime import timedelta, datetime, date
import logging
from todoist_api_python.models import Due, Task

from constants import LENGTH_CONTENT

def removeZ(date_str: str) -> str:
    return date_str.replace("Z", "")

def addZ(date_str: str):
    return date_str + "Z"

def timezoneF(date_task, timezone = None):
    if not timezone: 
        date_task = date_task - timedelta(hours=3)
    return date_task

def plusDaysDatetime(date_string, days, timezone = None): 
    date_from_today = todayDatetime(date_string)
    date_string_without_z = removeZ(date_from_today)
    logging.info(f"{date_string} : {date_string_without_z}")
    logging.info(f"Timezone: {timezone}")
    date_task = timezoneF(datetime.fromisoformat(date_string_without_z) + timedelta(days=int(days)))
    
    return addZ((date_task).isoformat())

def todayDatetime(date_string, timezone = None):
    date_string_without_z = removeZ(date_string)
    today = date.today()
    date_task = timezoneF(datetime.fromisoformat(date_string_without_z).replace(year=today.year, month=today.month, day=today.day), timezone)
    logging.info(f"date_task: {date_task.isoformat()}")
    return addZ(date_task.isoformat())

def minusDaysDatetime(date_string, days, timezone = None): 
    date_from_today = todayDatetime(date_string)
    date_string_without_z = removeZ(date_from_today)
    logging.info(f"{date_string} : {date_string_without_z}")
    date_task = timezoneF(datetime.fromisoformat(date_string_without_z) - timedelta(days=int(days)), timezone)
    return addZ((date_task).isoformat())

def plusDaysDate(date_string, days): 
    date_from_today = todayDate(date_string)
    logging.info(f"plusDaysDate({date_string}, {days})")
    return (date.fromisoformat(date_from_today) + timedelta(days=int(days))).isoformat()

def todayDate(date_string):
    today = date.today()
    task_date = date.fromisoformat(date_string).replace(year=today.year, month=today.month, day=today.day)
    return task_date.isoformat()

def minusDaysDate(date_string, days): 
    date_from_today = todayDate(date_string)
    logging.info(f"plusDaysDate({date_string}, {days})")
    return (date.fromisoformat(date_from_today) - timedelta(days=int(days))).isoformat()

def addZero(elem):
    if elem <= 9:
        return f"0{elem}"
    return f"{elem}"

def getTimeDatetime(dueDate: Due) -> str:
    if dueDate:
        date_string = dueDate.date
        if dueDate.datetime:
            date_string = dueDate.datetime
            date_string_without_z = removeZ(date_string)
            date_task = datetime.fromisoformat(date_string_without_z)
            if dueDate.timezone:
                date_task += timedelta(hours=3)
            day = f"{addZero(date_task.day)}"
            month = f"{addZero(date_task.month)}"
            hourRussia = f"{addZero(date_task.hour)}"
            minute = f"{addZero(date_task.minute)}"
            
            return f"{day}.{month} {hourRussia}:{minute}"
        else: 
            date_string_without_z = removeZ(date_string)
            date_task = date.fromisoformat(date_string_without_z)

            return f" | {date_task.day}.{date_task.month}"
    else: 
        return ""

def getTimeZone():
    return datetime.now().tzname()

def getTime(dueDate: Due):
    date_task = datetime.now() + timedelta(days=99)
    if dueDate:
        date_task = datetime.fromisoformat(removeZ(dueDate.date)).replace(hour = 23, minute = 59, second = 59)
        if(dueDate and dueDate.datetime):
            date_string_without_z = removeZ(dueDate.datetime)
            date_task = datetime.fromisoformat(date_string_without_z)
            if dueDate.timezone:
                date_task += timedelta(hours=3)

    return date_task

def getDueDate(task: Task): 
    due_str = "None"
    if task.due:
        due_str = f"Task - {task.id}, content - {task.content[:LENGTH_CONTENT]} ==== {task.due.__dict__} ++++"
    return due_str