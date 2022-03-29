import json

from flask import session

from entities.AliceRequest import AliceRequest

class AliceResponse:
    """Класс AliceResponse предназначен для реализации удобного интерфейса взаимодействия
    с ответом Алисы.
    -------------------------------------------------------------------------------------
    Задача класса - предоставлять удобный доступ к компонентам ответа Алисы.
    -------------------------------------------------------------------------------------
    Методы
        set_answer() - задает ответ Алисы в текстовом формате.
        end_session() - закрывает сессию с пользователем.
        to_json() - возвращает ответ Алисы в json формате.
        set_suggests() - прикрепляет варианты ответа для пользователя (кнопки).
        set_image() - прикрепляет картинку к ответу.
    """

    def __init__(self, request: AliceRequest, state):
        """Конструктор класса принимает аргумента класса AliceRequest для установки версии и сессии
        для ответа."""
        
        self._response = {
            "application_state": request.state_application,
            "version": request.version,
            "session": request.session,
            "response": {"end_session": False},
        }
        
        self.set_current_state(request.user_id, state)

    def set_auth(self):
        del self._response["response"]
        self._response["start_account_linking"] = {}

    def set_answer(self, answer):
        self._response["response"]["text"] = answer

    def set_say_answer(self, answer):
        self._response["response"]["tts"] = answer

    def end_session(self):
        user_id = self._response["session"]["user_id"]
        self._response["application_state"][user_id] = "HelloState"
        self._response["response"]["end_session"] = True

    def to_json(self):
        user_id = self._response["session"]["user_id"]
        
        self._response["application_state"][user_id] = str(self._response["application_state"][user_id])

        return json.dumps(self._response)

    def set_suggests(self, suggests):
        self._response["response"]["buttons"] = suggests

    def set_image(self, image):
        self._response["response"]["card"] = image

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return self.to_json()

    def set_current_state(self, user_id, state):
        self._response["application_state"][user_id] = state

    def set_str_state(self, state):
        user_id = self._response["session"]["user_id"]
        self._response["application_state"][user_id] = state

    def get_application_state(self):
        user_id = self._response["session"]["user_id"]
        return self._response["application_state"].get(user_id)

        
