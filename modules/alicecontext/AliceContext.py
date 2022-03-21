import logging

from entities.AliceRequest import AliceRequest
from entities.AliceResponse import AliceResponse

EXIT_WORDS = {'выход', 'пока', 'выйти', 'уйти', 'покинуть'}
YES_WORDS = {'да', 'конечно', 'ок', 'хорошо', 'погнали'}

class AliceContext:
    """Класс Context предназначен для управления состояниями навыка Алисы.
    ---------------------------------------------------------------------
    Методы
        transition_to(state) - переключает контекст в состояние state
        handle_dialog(res, req) - основная функция для управления диалогом с пользователем.
            res: AliceResponse - ответ для пользователя в виде класса AliceResponse
            req: AliceRequest - запрос пользователя в виде класса AliceRequest"""
    _state = None

    def __init__(self, state):
        self.transition_to(state)

    def transition_to(self, state):
        logging.info(f'Context: переключаемся в {type(state).__name__}')
        self._state = state
        self._state.context = self

    def handle_dialog(self, res: AliceResponse, req: AliceRequest):
        self._state.handle_dialog(res, req)


    def __str__(self) -> str:
        return str(self._state)

    def __repr__(self) -> str:
        return str(self._state)