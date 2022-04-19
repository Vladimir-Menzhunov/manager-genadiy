from datetime import timedelta, datetime, date
import logging
from sqlite3 import Timestamp

def removeZ(date_str: str) -> str:
    return date_str.replace("Z", "")

def addZ(date_str: str):
    return date_str + "Z"

def plusDaysDatetime(date_string, days): 
    date_from_today = todayDatetime(date_string)
    date_string_without_z = removeZ(date_from_today)
    logging.info(f"{date_string} : {date_string_without_z}")
    return addZ((datetime.fromisoformat(date_string_without_z) + timedelta(days=int(days)) - timedelta(hours=3)).isoformat())

def todayDatetime(date_string):
    date_string_without_z = removeZ(date_string)
    today = date.today()
    date_task = datetime.fromisoformat(date_string_without_z).replace(year=today.year, month=today.month, day=today.day)
    logging.info(f"date_task: {date_task.isoformat()}")
    return addZ(date_task.isoformat())

def minusDaysDatetime(date_string, days): 
    date_from_today = todayDatetime(date_string)
    date_string_without_z = removeZ(date_from_today)
    logging.info(f"{date_string} : {date_string_without_z}")
    return addZ((datetime.fromisoformat(date_string_without_z) - timedelta(days=int(days), hours=3)).isoformat())

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

def getTimeDatetime(date_string) -> str:
    date_string_without_z = removeZ(date_string)
    date_task = datetime.fromisoformat(date_string_without_z) + timedelta(hours=3)
    hourRussia = f"{date_task.hour}"
    minute = date_task.minute
    if date_task.minute <= 9:
        minute = f"0{date_task.minute}"
    
    result = f"{hourRussia}:{minute}"
    return result

def getTimeZone():
    return datetime.now().tzname()

def getTime(date_string):
    date_task = datetime.now() + timedelta(days=1)
    if(date_string and date_string.datetime):
        date_string_without_z = removeZ(date_string.datetime)
        date_task = datetime.fromisoformat(date_string_without_z) + timedelta(hours=3)

    return date_task