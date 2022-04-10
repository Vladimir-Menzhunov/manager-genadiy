import logging
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
            project_name = req.get_project_name_for_task
            logging.info(f"project_name_for_task: {project_name}")
            task_entity = todoist.get_list_task_name_by_project_and_time(project_name = project_name)
            res.set_say_answer("У вас {} задач".format(task_entity.len))
            res.set_answer(task_entity.tasks)
            return
        elif req.project_list:
            project_entity = todoist.get_list_project_name()
            res.set_say_answer("У вас {} проектов".format(project_entity.len))
            res.set_answer(project_entity.projects)
        elif len(req.words) == 0:
            res.set_answer("Рад тебя снова видеть братишка! Что спланируем сегодня?")
        else: 
            res.set_answer("Я так не умею, можешь воспользоваться примерами из подсказок =)")
            res.set_suggests([
                {'title': 'Выйти', 'hide': True},
                {'title': 'Список задач', 'hide': True},
                {'title': 'Задачи в покупках', 'hide': True},
                {'title': 'Список проектов', 'hide': True},
            ])
            return
        
        res.set_suggests([
            {'title': 'Выйти', 'hide': True},
        ])

    def __str__(self):
        return "ChoiceState"

    def __repr__(self):
        return "ChoiceState"
