from email.mime import application
import json
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

    def __init__(self, request: AliceRequest):
        """Конструктор класса принимает аргумента класса AliceRequest для установки версии и сессии
        для ответа."""
        application_state = {}
        if request.state:
            application_state = request.state_application
        self._response = {
            "version": request.version,
            "session": request.session,
            "response": {"end_session": False},
            "application_state": application_state,
        }

    def set_answer(self, answer):
        self._response["response"]["text"] = answer

    def end_session(self):
        self._response["response"]["end_session"] = True

    def to_json(self):
        return json.dumps(self._response)

    def set_suggests(self, suggests):
        self._response["response"]["buttons"] = suggests

    def set_image(self, image):
        self._response["response"]["card"] = image

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return self.to_json()
