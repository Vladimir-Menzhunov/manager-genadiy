from calendar import month
from datetime import datetime, timedelta
import logging
import unittest
from additionalfunction.TimeHelper import DateSettings, DayMonth, FromToDateTime, getDueDate, getTimeZone, minusDaysDate, minusDaysDatetime, plusDaysDate, plusDaysDatetime, todayDate, todayDatetime
from additionalfunction.comparefunc import cosine_compare
from todoist_api_python.api import TodoistAPI
from additionalfunction.processing_contents import processing_task
from entities.AliceRequest import AliceRequest
from entities.AliceResponse import AliceResponse
from entities.AliceTodoist import AliceTodoist, build_task_entity
from main import get_current_state
from modules.alicestates.AliceState import AliceState
from modules.alicestates.ChoiceState import ChoiceState
from modules.alicestates.HelloState import HelloState

"""
покажи список просроченных задач
покажи список просроченных задач в покупках
просроченные задачи в покупках
просроченные задачи
покажи что просрочено в покупках
покажи что просроченно
список проектов 
покажи проекты 
покажи какие есть проекты
Перенеси просроченные задачи
Перенос просроченных задач
Перенос просроченных задач на сегодня
Перенос просроченных дел в покупках
Перенос просроченных задач в работе 
перенеси просроченные задачи в работе на послезавтра
задачи в ближайшие 3 часа
задачи в покупках на ближайшие 3 часа 
задачи в покупках на ближайший час
задачи в покупках на ближайший день
задачи в покупках ближайшие 3 часа
Список задач
Список Дел
список задач в покупках
список дел в покупках
что есть в идеях 
Список задач на сегодня
задачи в покупках 
покажи задачи в покупках
покажи что в покупках
покажи задачи на завтра 
покажи задачи на вчера
покажи задачи которые были вчера
покажи задачи в работе на завтра 

покажи регулярные задачи
покажи регулярные задачи в работе
какие регулярные задачи в работе
какие есть регулярные задачи в работе
регулярные задачи в работе
покажи нерегулярные задачи
покажи нерегулярные задачи в работе
какие нерегулярные задачи в работе
какие есть нерегулярные задачи в работе
нерегулярные задачи в работе
список регулярных задач
"""

reqNoAuth = {
    "meta": {
        "locale": "ru-RU",
        "timezone": "UTC",
        "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
        "interfaces": {
                    "screen": {},
                    "payments": {},
                    "account_linking": {}
        }
    },
    "session": {
        "message_id": 1,
        "session_id": "f402cc25-e962-4db0-a112-2d4e9ee69ad6",
        "skill_id": "2d9ef5db-7b49-45f6-94bd-1152cb0ca9eb",
        "user": {
                    "user_id": "748E450E1C6B760F4DF2F0FAB4792A4A0FC2D285B2E4A7989E23B8942AF8E5B5"
        },
        "application": {
            "application_id": "CC11972A3499029C5A37AD8EACAD223466CC784E59DFA4B687087E93C820280A"
        },
        "user_id": "CC11972A3499029C5A37AD8EACAD223466CC784E59DFA4B687087E93C820280A",
        "new": False
    },
    "request": {
        "command": "jj",
        "original_utterance": "jj",
        "nlu": {
            "tokens": [
                "jj"
            ],
            "entities": [],
            "intents": {}
        },
        "markup": {
            "dangerous_context": False
        },
        "type": "SimpleUtterance"
    },
    "state": {
        "application": {
            "value": 37
        }
    },
    "version": "1.0"
}

reqAuthWithoutState = {
    "meta": {
        "locale": "ru-RU",
        "timezone": "UTC",
        "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
        "interfaces": {
                    "screen": {},
                    "payments": {},
                    "account_linking": {}
        }
    },
    "session": {
        "message_id": 1,
        "session_id": "f402cc25-e962-4db0-a112-2d4e9ee69ad6",
        "skill_id": "2d9ef5db-7b49-45f6-94bd-1152cb0ca9eb",
        "user": {
                    "user_id": "748E450E1C6B760F4DF2F0FAB4792A4A0FC2D285B2E4A7989E23B8942AF8E5B5",
                    "access_token": "5c18c67296103ec880d256e7411687246badbe21"
        },
        "application": {
            "application_id": "CC11972A3499029C5A37AD8EACAD223466CC784E59DFA4B687087E93C820280A"
        },
        "user_id": "CC11972A3499029C5A37AD8EACAD223466CC784E59DFA4B687087E93C820280A",
        "new": False
    },
    "request": {
        "command": "jj",
        "original_utterance": "jj",
        "nlu": {
            "tokens": [
                "jj"
            ],
            "entities": [],
            "intents": {}
        },
        "markup": {
            "dangerous_context": False
        },
        "type": "SimpleUtterance"
    },
    "state": {
        "session": {},
        "user": {},
        "application": {}
    },
    "version": "1.0"
}

requestWithDates = {
  "meta": {
    "locale": "ru-RU",
    "timezone": "UTC",
    "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
    "interfaces": {
      "screen": {},
      "payments": {},
      "account_linking": {}
    }
  },
  "session": {
    "message_id": 21,
    "session_id": "667941e8-48a6-4328-bdd9-3fe259fe284e",
    "skill_id": "2d9ef5db-7b49-45f6-94bd-1152cb0ca9eb",
    "user": {
      "user_id": "748E450E1C6B760F4DF2F0FAB4792A4A0FC2D285B2E4A7989E23B8942AF8E5B5",
      "access_token": "48f85b6a0c1d2727ea813412f7af844c6d7a331c"
    },
    "application": {
      "application_id": "CC11972A3499029C5A37AD8EACAD223466CC784E59DFA4B687087E93C820280A"
    },
    "user_id": "CC11972A3499029C5A37AD8EACAD223466CC784E59DFA4B687087E93C820280A",
    "new": False
  },
  "request": {
    "command": "перенос просроченных задач на завтра",
    "original_utterance": "перенос просроченных задач на завтра ",
    "nlu": {
      "tokens": [
        "перенос",
        "просроченных",
        "задач",
        "на",
        "завтра"
      ],
      "entities": [
        {
          "type": "YANDEX.DATETIME",
          "tokens": {
            "start": 3,
            "end": 5
          },
          "value": {
            "day": 1,
            "day_is_relative": True
          }
        }
      ],
      "intents": {
        "RESCHEDULE.TASK": {
          "slots": {
            "type": {
              "type": "YANDEX.STRING",
              "tokens": {
                "start": 2,
                "end": 3
              },
              "value": "задач"
            }
          }
        }
      }
    },
    "markup": {
      "dangerous_context": False
    },
    "type": "SimpleUtterance"
  },
  "state": {
    "session": {},
    "user": {},
    "application": {
      "CC11972A3499029C5A37AD8EACAD223466CC784E59DFA4B687087E93C820280A": "ChoiceState"
    }
  },
  "version": "1.0"
}

"""
    Все объекты изменяемы, поэтому лучше новый набор данных для каждого AliceRequest и AliceResponse
"""
class AliceRequestTest(unittest.TestCase):
    def test_get_session_access_token(self):

        aliceReq = AliceRequest(reqNoAuth)
        self.assertEqual(aliceReq.access_token, None)

        aliceReq = AliceRequest(reqAuthWithoutState)
        self.assertEqual(aliceReq.access_token, "5c18c67296103ec880d256e7411687246badbe21")

        self.assertEqual(reqAuthWithoutState["state"]["application"].get(aliceReq.user_id), None)


class AliceResponceTest(unittest.TestCase):
    def test_get_state_application(self):
        aliceReq = AliceRequest(reqAuthWithoutState)
        state = get_current_state(aliceReq)
        aliceRes = AliceResponse(aliceReq, state)

        self.assertEqual(str(reqAuthWithoutState["state"]["application"].get(aliceReq.user_id)), "HelloState")

        self.assertEqual(
            str(aliceRes._response["application_state"][aliceReq.user_id]), "HelloState")

        aliceReq = AliceRequest(reqNoAuth)
        aliceRes = AliceResponse(aliceReq, state)

        self.assertEqual(aliceRes._response["application_state"]["value"], 37)

        aliceRes._response["application_state"]["value1"] = 45

        self.assertEqual(aliceRes._response["application_state"]["value1"], 45)

    def test_handle_dialog(self):
        aliceReq = AliceRequest(reqAuthWithoutState)
        state = get_current_state(aliceReq)
        self.assertEqual(bool({"x": 1}), True)
        aliceRes = AliceResponse(aliceReq, state)
        user_id = aliceRes._response["session"]["user_id"]
        self.assertEqual(
            str(aliceRes._response["application_state"][user_id]), "HelloState")
        self.assertTrue(isinstance(
            aliceRes._response["application_state"][user_id]._state, HelloState))
        alice_todoist = None
        if(aliceReq.access_token):
            alice_todoist = AliceTodoist(aliceReq)
        aliceRes.get_application_state().handle_dialog(aliceRes, aliceReq, alice_todoist)
        self.assertTrue(isinstance(
            aliceRes._response["application_state"][user_id]._state, ChoiceState))

        self.assertEqual(str(reqAuthWithoutState["state"]["application"].get(aliceReq.user_id)), "ChoiceState")


class TestForOtherFunction(unittest.TestCase):
    def test_function_main(self):
        aliceReq = AliceRequest(reqAuthWithoutState)
        state = get_current_state(aliceReq)
        aliceRes = AliceResponse(aliceReq, state)
        user_id = aliceRes._response["session"]["user_id"]
        self.assertEqual(
            str(aliceRes._response["application_state"][user_id]), "ChoiceState")
        self.assertTrue(isinstance(
            aliceRes._response["application_state"][user_id]._state, AliceState))

class TestSklern(unittest.TestCase):
    def test_sklern_cosine_compare(self):

        print(cosine_compare("Английский язык", "английском"))
        print(cosine_compare("Работа", "работе"))
        self.assertTrue(cosine_compare("Английский язык", "Английский") >= 0.88642)
        self.assertTrue(cosine_compare("Английский", "ggggggg") == 0.)

class TestTodoist(unittest.TestCase):
    def test_todoist(self):
        app = TodoistAPI("5c18c67296103ec880d256e7411687246badbe21")
        print(app.get_projects())
        self.assertTrue(1 == 1)

class TestDueDatetime(unittest.TestCase):
    def test_correct_datetime(self):
        date_string = "2011-11-04T00:05:23"
        days = 1
        date = "2011-11-04"

        today = datetime.now().replace(hour=0, minute=5, second=23, microsecond=0)
        tomorrow = today + timedelta(days=1)
        todayDate = todayDatetime(date_string, "timezone")
        self.assertEqual(todayDate, f"{today.isoformat()}Z")
        self.assertEqual(plusDaysDatetime(date_string, 1, "timezone"), f"{tomorrow.isoformat()}Z")
        # self.assertEqual(minusDaysDatetime(date_string, 1), f"2022-04-17T21:05:23Z")
        # self.assertEqual(plusDaysDate(date, 1), "2022-04-20")
        # self.assertEqual(minusDaysDate(date, 1), "2022-04-18")
        
        
        req = AliceRequest(reqAuthWithoutState)
        todoist = AliceTodoist(req)
        rescheduled_tasks = todoist.get_list_task_name_by_project_and_time() #.reschedule_tasks()
        #rescheduled_tasks = todoist.reschedule_tasks("работе")
        #tasks = todoist.todoist.get_tasks(filter = "overdue")
        
        print("Мы перенесли {}".format(processing_task(rescheduled_tasks.len)))
        print(rescheduled_tasks.tasks)

class TestProcessTask(unittest.TestCase):
    def test_process_task(self):
        count1 = 1
        count2 = 2
        count3 = 5

        self.assertEqual(processing_task(count1), "1 задача")
        self.assertEqual(processing_task(count2), "2 задачи")
        self.assertEqual(processing_task(count3), "5 задач")

class TestDates(unittest.TestCase):
    def test_dates(self):
        req = AliceRequest(requestWithDates)
        self.assertEqual(req.dates[0]["day"], 1)

    def timezone(self):

        print(getTimeZone())

class TestCheckDueForTask(unittest.TestCase):
    def checkDueTask(self):
        req = AliceRequest(reqAuthWithoutState)
        todoist = AliceTodoist(req)
        list_tasks = todoist.get_list_tasks("today")
        for task in list_tasks: 
            logging.info(getDueDate(task))
        
        self.assertEqual(1, 1)

    def checkGetTime(self):
        req = AliceRequest(reqAuthWithoutState)
        todoist = AliceTodoist(req)
        list_tasks = todoist.get_list_tasks("overdue")
        logging.info(build_task_entity(list_tasks).__dict__)
        
        self.assertEqual(1, 1)

class GetTasksTest(unittest.TestCase):
    def getTaskByDate(self):
        req = AliceRequest(reqAuthWithoutState)
        todoist = AliceTodoist(req)
        
        fromToTime = FromToDateTime(hours=4)
        #due before: +8 hours & !overdue
        list_tasks = todoist.get_list_tasks(f"due before: +8 hours & !overdue")
        logging.info(build_task_entity(list_tasks).__dict__)
        
        logging.info(datetime.now().isoformat())
        logging.info(datetime.now().date() + timedelta(days = -1))
        self.assertEqual(1, 1)

    def getReccuring(self):
        req = AliceRequest(reqAuthWithoutState)
        todoist = AliceTodoist(req)
        today = minusDaysDate(1)
        #listTask = self.todoist.get_tasks(project_id = got_project_id, filter=f"due before: {today}")
        #due before: +8 hours & !overdue
        logging.info(f"today: {today}")
        list_tasks = todoist.get_list_tasks(project_id="2258361766", filter = f"due after: {today} & !recurring")
        logging.info(build_task_entity(list_tasks).__dict__)
        self.assertEqual(1, 1)

    def getTaskByTime(self):
        req = AliceRequest(reqAuthWithoutState)
        todoist = AliceTodoist(req)

        dayMonth = DayMonth(day=15, month=6)
        date = "2011-11-04"
        timeZone = None
        todayDatetime(date, timeZone, dayMonth=dayMonth)
        logging.info(todayDatetime)
        self.assertEqual(1, 1)
      
    def getTaskId(self):
        req = AliceRequest(reqAuthWithoutState)
        todoist = AliceTodoist(req)

        list_tasks = todoist.get_list_tasks()
        logging.info(list_tasks)
        self.assertEqual(1, 1)

    def addTask(self):
      req = AliceRequest(reqAuthWithoutState)
      todoist = AliceTodoist(req)

      #add = todoist.add_task(None, ["огурцы"], DateSettings())
      #add = todoist.add_task(None, ["огурцы"], DateSettings(day=1))
      #add = todoist.add_task(None, ["огурцы"], DateSettings(day=1, hour=15))
      #add = todoist.add_task(None, ["огурцы"], DateSettings(day=1, hour=15, minute=16))
      #add = todoist.add_task(None, ["огурцы"], DateSettings(day=1, hour=15, minute=16, month=8))
      #logging.info(add)
      self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
# python3 -m unittest tests.GetTasksTest.addTask
 