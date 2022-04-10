import unittest
from additionalfunction.compatefunc import cosine_compare
from todoist_api_python.api import TodoistAPI
from entities.AliceRequest import AliceRequest
from entities.AliceResponse import AliceResponse
from entities.AliceTodoist import AliceTodoist
from main import get_current_state
from modules.alicestates.AliceState import AliceState
from modules.alicestates.ChoiceState import ChoiceState
from modules.alicestates.HelloState import HelloState

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
        self.assertTrue(cosine_compare("Английский язык", "Английский") == 1.)
        self.assertTrue(cosine_compare("Английский", "ggggggg") == 0.)

class TestTodoist(unittest.TestCase):
    def test_todoist(self):
        app = TodoistAPI("5c18c67296103ec880d256e7411687246badbe21")
        print(app.get_projects())
        self.assertTrue(1 == 1)

if __name__ == '__main__':
    unittest.main()
# python -m unittest tests.TestSklern.test_sklern_cosine_compare 