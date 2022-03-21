from entities.AliceRequest import AliceRequest
from entities.AliceResponse import AliceResponse
from modules.alicecontext.AliceContext import EXIT_WORDS
from modules.alicestates.AliceState import AliceState


class ChoiceState(AliceState):
    def handle_dialog(self, res: AliceResponse, req: AliceRequest):
        if set(req.words).intersection(EXIT_WORDS):
            res.set_answer('Пока!')
            res.end_session()
            return
        elif req.task_list: 
            #TODO список задач
            res.set_answer('Просмотр списка задач!')
            return
        
        
        res.set_suggests([{'title': 'Выйти', 'hide': True}])

    def __str__(self):
        return "ChoiceState"

    def __repr__(self):
        return "ChoiceState"
