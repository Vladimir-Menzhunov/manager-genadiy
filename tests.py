import unittest

from entities.AliceRequest import AliceRequest
from entities.AliceResponse import AliceResponse

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

reqAuth = {
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
                    "access_token": "Hello"
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
            "version": "1.0"
        }

class AliceRequestTest(unittest.TestCase):
    def test_get_session_access_token(self):
        
        aliceReq = AliceRequest(reqNoAuth)
        self.assertEqual(aliceReq.access_token, None)

        aliceReq = AliceRequest(reqAuth)
        self.assertEqual(aliceReq.access_token, "Hello")

        self.assertEqual(aliceReq.state_application, "")

class AliceResponceTest(unittest.TestCase):
    def test_get_state_application(self):
        aliceReq = AliceRequest(reqAuth)
        aliceRes = AliceResponse(aliceReq)

        self.assertEqual(aliceRes._response["application_state"], {})

if __name__ == '__main__':
    unittest.main()
