from entities.AliceRequest import AliceRequest
from entities.AliceResponse import AliceResponse
from modules.alicestates.AliceState import AliceState
from modules.alicestates.AuthState import AuthState
from modules.alicestates.ChoiceState import ChoiceState


class HelloState(AliceState):
    
    def handle_dialog(self, res: AliceResponse, req: AliceRequest):
        if not req.access_token:
            res.set_answer('Менеджер Геннадий, позволяет вам буквально одной фразой добавлять записи в Todoist, а также получать сводку событий на любой период.\n\nНачать связываение аккаунтов?')
            res.set_suggests([{'title': 'Да', 'hide': True}, {'title': 'Нет', 'hide': True}])
            self.context.transition_to(AuthState())
        else:
            res.set_answer('Что бы вы хотели узнать или добавить?')
            res.set_suggests([{'title': 'Помощь', 'hide': True}, {'title': 'Список дел', 'hide': True}])
            self.context.transition_to(ChoiceState())

    def __str__(self):
        return "HelloState"

    def __repr__(self):
        return "HelloState"