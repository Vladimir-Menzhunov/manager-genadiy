from entities.AliceRequest import AliceRequest
from entities.AliceResponse import AliceResponse
from entities.AliceTodoist import AliceTodoist
from modules.alicecontext.AliceContext import EXIT_WORDS
from modules.alicestates.AliceState import AliceState

class ChoiceState(AliceState):
    def handle_dialog(self, res: AliceResponse, req: AliceRequest, todoist: AliceTodoist):
        if set(req.words).intersection(EXIT_WORDS):
            res.set_answer('Пока!')
            res.end_session()
            return
        elif req.task_list: 
            #TODO список задач
            res.set_answer('Просмотр списка задач!')
            return
        elif req.project_list:
            res.set_answer(todoist.get_list_project_name())
        else:
            res.set_answer("Я так не умею, вы можете посмотреть на список проектов или задач на сегодня")
        
        res.set_suggests([{'title': 'Выйти', 'hide': True}])

    def __str__(self):
        return "ChoiceState"

    def __repr__(self):
        return "ChoiceState"
