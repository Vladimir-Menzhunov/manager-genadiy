from abc import ABC, abstractmethod
from entities.AliceRequest import AliceRequest
from entities.AliceResponse import AliceResponse
from modules.alicecontext.AliceContext import AliceContext

class AliceState(ABC):
    """Базовый абстрактный класс состояния.
     --------------------------------------
     Методы
        context - возвращает используемый данным состоянием контекст
        handle_dialog(res: req) - функция, которую вызывает контекст, для обработки диалога
        с пользователем"""

    @property
    def context(self) -> AliceContext:
        return self._context

    @context.setter
    def context(self, context: AliceContext) -> None:
        self._context = context

    @abstractmethod
    def handle_dialog(self, res: AliceResponse, req: AliceRequest):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass