from datetime import timedelta, datetime, date
import logging

def removeZ(date_str: str) -> str:
    return date_str.replace("Z", "")

def addZ(date_str: str):
    return date_str + "Z"

def plusDaysDatetime(date_string, days): 
    date_from_today = todayDatetime(date_string)
    date_string_without_z = removeZ(date_from_today)
    #logging.info(f"{date_string} : {date_string_without_z}")
    return addZ((datetime.fromisoformat(date_string_without_z) + timedelta(days=int(days))).isoformat())

def todayDatetime(date_string):
    date_string_without_z = removeZ(date_string)
    today = date.today()
    date_task = datetime.fromisoformat(date_string_without_z).replace(year=today.year, month=today.month, day=today.day)
    
    return addZ(date_task.isoformat())

def minusDaysDatetime(date_string, days): 
    date_from_today = todayDatetime(date_string)
    date_string_without_z = removeZ(date_from_today)
    #logging.info(f"{date_string} : {date_string_without_z}")
    return addZ((datetime.fromisoformat(date_string_without_z) - timedelta(days=int(days))).isoformat())

def plusDaysDate(date_string, days): 
    date_from_today = todayDate(date_string)
    #logging.info(f"plusDaysDate({date_string}, {days})")
    return (date.fromisoformat(date_from_today) + timedelta(days=int(days))).isoformat()

def todayDate(date_string):
    today = date.today()
    task_date = date.fromisoformat(date_string).replace(year=today.year, month=today.month, day=today.day)
    return task_date.isoformat()

def minusDaysDate(date_string, days): 
    date_from_today = todayDate(date_string)
    #logging.info(f"plusDaysDate({date_string}, {days})")
    return (date.fromisoformat(date_from_today) - timedelta(days=int(days))).isoformat()

