from datetime import timedelta, datetime, date
import logging
from todoist_api_python.models import Due, Task

from constants import LENGTH_CONTENT
from entities.AliceRequest import AliceRequest

class DayMonth:
    def __init__(self, day = None, month = None):
        self.day = day
        self.month = month

def removeZ(date_str: str) -> str:
    return date_str.replace("Z", "")

def addZ(date_str: str):
    return date_str + "Z"

def timezoneF(date_task, timezone = None):
    if not timezone: 
        date_task = date_task - timedelta(hours=3)
    return date_task

def plusDaysDatetime(date_string, days, timezone = None): 
    date_from_today = todayDatetime(date_string, timezone)
    date_string_without_z = removeZ(date_from_today)
    logging.info(f"{date_string} : {date_string_without_z}")
    logging.info(f"Timezone: {timezone}")
    date_task = datetime.fromisoformat(date_string_without_z) + timedelta(days=int(days))
    
    return addZ((date_task).isoformat())

def todayDatetime(date_string, timezone = None, dayMonth: DayMonth = None):
    date_string_without_z = removeZ(date_string)
    today = date.today()
    if dayMonth:
        today = today.replace(month=dayMonth.month, day=dayMonth.day)
    logging.info(f"today - {today}")
    date_task = timezoneF(datetime.fromisoformat(date_string_without_z).replace(year=today.year, month=today.month, day=today.day), timezone)
    logging.info(f"date_task: {date_task.isoformat()}")
    return addZ(date_task.isoformat())

def minusDaysDatetime(date_string, days, timezone = None): 
    date_from_today = todayDatetime(date_string, timezone)
    date_string_without_z = removeZ(date_from_today)
    logging.info(f"{date_string} : {date_string_without_z}")
    date_task = datetime.fromisoformat(date_string_without_z) - timedelta(days=int(days))
    return addZ((date_task).isoformat())

def plusDaysDate(date_string, days): 
    date_from_today = todayDate()
    logging.info(f"plusDaysDate({date_string}, {days})")
    return (date.fromisoformat(date_from_today) + timedelta(days=int(days))).isoformat()

# Меняем у даты день и месяц в случае передачи dayMonth
def todayDate(dayMonth: DayMonth = None):
    today = date.today()
    if dayMonth:
        today = today.replace(day=dayMonth.day, month=dayMonth.month)
    return today.isoformat()

def minusDaysDate(days): 
    date_from_today = todayDate()
    logging.info(f"minusDaysDate({date_from_today}, {days})")
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
            
            return f" | {day}.{month} {hourRussia}:{minute}"
        else: 
            date_string_without_z = removeZ(date_string)
            date_task = date.fromisoformat(date_string_without_z)

            return f" | {addZero(date_task.day)}.{addZero(date_task.month)}"
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

def getDateForFilter(dayMonthCount: DayMonth):
    if dayMonthCount.month:
        dateForFilter = datetime.now().date()
        return dateForFilter.replace(day=dayMonthCount.day, month=dayMonthCount.month)
    else:    
        if dayMonthCount.day or dayMonthCount.day == 0:
            dateForFilter = datetime.now().date() + timedelta(days = dayMonthCount.day)
            return dateForFilter
        else: 
            return None
    
class FromToDateTime:
    def __init__(self, hours):
        now = datetime.now()
        toTime = now + timedelta(hours=hours)
        self.fromTime = now.isoformat()
        self.toTime = toTime.isoformat()

def getHours(req: AliceRequest):
    #day = 0
    hour = 0
    #month = 0
    if len(req.dates) > 0:
        # if req.dates[0].get("day"):
        #     day = req.dates[0].get("day")
        if req.dates[0].get("hour"):
            hour = req.dates[0].get("hour")
        # if req.dates[0].get("month"):
        #     month = req.dates[0].get("month")
    #logging.info(f"day: {day}")
    logging.info(f"hour: {hour}")
    #logging.info(f"month: {month}")

    return hour
    
def getDayMonth(req: AliceRequest):
    #TODO - формирование дней и месяцев для получения задач по конкретной дате, если есть месяц, то считать конкретной датой
    dayTime = None
    month = None
    if len(req.dates) > 0:
        if req.dates[0].get("day"):
            dayTime = req.dates[0].get("day")
        if req.dates[0].get("month"):
            month = req.dates[0].get("month")
    logging.info(f"dayTime: {dayTime}")
    logging.info(f"month: {month}")
    return DayMonth(day=dayTime, month=month)

class DateSettings:
    def __init__(self, day = None, month = None, hour = None, minute = None) -> None:
        self.day = day
        self.month = month
        self.hour = hour
        self.minute = minute
        self.recurring = False

        temp_datetime = None
        temp_date = None
        # Если пришёл только день - завтра, послезавтра
        # Если пришли только часы, то это сегодня в X часов
        # если пришел месяц, то это конкретная дата, есть часы datetime - нет date
        if month:
            if hour:
                if minute:
                    temp_datetime = datetime.today().replace(day=day, month=month, hour=hour, minute=minute, microsecond=0)
                    temp_date = temp_datetime.date()
                else:
                    temp_datetime = datetime.today().replace(day=day, month=month, hour=hour, minute=0, microsecond=0)
                    temp_date = temp_datetime.date()
            else: 
                temp_date = date.today().replace(day=day, month=month)
        elif day:
            if hour:
                if minute:
                    temp_datetime = datetime.today().replace(hour=hour, minute=minute, microsecond=0) + timedelta(days=day)
                    temp_date = temp_datetime.date()
                else:
                    temp_datetime = datetime.today().replace(hour=hour, minute=0, microsecond=0) + timedelta(days=day)
                    temp_date = temp_datetime.date()
            else: 
                temp_date = date.today() + timedelta(days=day)
        
        self.datetime = temp_datetime
        self.date = temp_date
        self.timezone = 'Europe/Moscow'

def getDateSettings(req: AliceRequest):
    day = None
    month = None
    hour = None
    minute = None
    if len(req.dates) > 0:
        if req.dates[0].get("day"):
            day = req.dates[0].get("day")
        if req.dates[0].get("month"):
            month = req.dates[0].get("month")
        if req.dates[0].get("hour"):
            hour = req.dates[0].get("hour")
        if req.dates[0].get("minute"):
            minute = req.dates[0].get("minute")
    logging.info(f"day: {day}")
    logging.info(f"month: {month}")
    logging.info(f"hour: {hour}")
    logging.info(f"minute: {minute}")

    return DateSettings(day = day, month = month, hour = hour, minute = minute)