import logging
import re
from additionalfunction.TimeHelper import getDay, getHours, getTimeZone
from additionalfunction.processing_contents import processing_overdue_task, processing_task
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
            logging.info(f"getTimeZone: {getTimeZone()}")
            project_name = req.get_project_name_for_task
            logging.info(f"project_name_for_task: {project_name}")
            dayTime = getDay(req)
            task_entity = todoist.get_list_task_name_by_project_and_time(project_name = project_name, dayTime = dayTime)
            if(task_entity.len != 0):
                res.set_say_answer("У вас {} задач".format(task_entity.len))
                res.set_answer(task_entity.tasks)
            elif task_entity.len == -1: 
                res.set_answer(task_entity.tasks)
                res.set_suggests([
                    {'title': 'Выйти', 'hide': True},
                    {'title': 'Создай проект Отдых', 'hide': True},
                    {'title': 'Создай проект Учеба', 'hide': True},
                ])
            else:
                res.set_answer("У вас нет задач, создадим задачу?")
                res.set_suggests([
                    {'title': 'Выйти', 'hide': True},
                    {'title': 'Добавь рыбу в покупки', 'hide': True},
                    {'title': 'Добавь практика языка в английский каждый день по 1 часу', 'hide': True},
                ])
            return
        elif req.project_list:
            project_entity = todoist.get_list_project_name()
            res.set_say_answer("У вас {} проектов".format(project_entity.len))
            res.set_answer(project_entity.projects)
        elif req.reschedule_task:
            project_name = req.get_project_name_for_reschedule
            logging.info(f"project_name_for_task: {project_name}")

            dayTime = getDay(req)
            
            rescheduled_tasks = todoist.reschedule_tasks(project_name = project_name, dayTime = dayTime)

            if(rescheduled_tasks.len != 0):
                res.set_say_answer("Мы перенесли {}".format(processing_task(rescheduled_tasks.len)))
                res.set_answer(rescheduled_tasks.tasks)
            elif rescheduled_tasks.len == -1: 
                res.set_answer(rescheduled_tasks.tasks)
                res.set_suggests([
                    {'title': 'Выйти', 'hide': True},
                    {'title': 'Создай проект Отдых', 'hide': True},
                    {'title': 'Создай проект Учеба', 'hide': True},
                ])
            else:
                res.set_answer("У вас нет просроченных задач!")

            return
        elif req.task_coming_hours:
            project_name = req.get_project_name_for_coming_hours
            logging.info(f"project_name_for_task: {project_name}")

            hours = getHours(req)
            logging.info(f"getHours: {hours}")

            task_entity = todoist.get_list_task_coming_hours_by_project_name(project_name = project_name, hours=hours)
            if(task_entity.len != 0):
                res.set_say_answer("У вас  {}".format(processing_task(task_entity.len)))
                res.set_answer(task_entity.tasks)
            elif task_entity.len == -1: 
                res.set_answer(task_entity.tasks)
                res.set_suggests([
                    {'title': 'Выйти', 'hide': True},
                    {'title': 'Создай проект Отдых', 'hide': True},
                    {'title': 'Создай проект Учеба', 'hide': True},
                ])
            else:
                res.set_answer("У вас нет задач, создадим задачу?")
                res.set_suggests([
                    {'title': 'Выйти', 'hide': True},
                    {'title': 'Добавь рыбу в покупки', 'hide': True},
                    {'title': 'Добавь практика языка в английский каждый день по 1 часу', 'hide': True},
                ])
            return
        elif req.overdue_task:
            project_name = req.get_project_name_overdue_task
            logging.info(f"project_name_for_task: {project_name}")
            
            task_entity = todoist.get_list_overdue_task(project_name = project_name)
            if(task_entity.len != 0):
                res.set_say_answer("У вас  {}".format(processing_overdue_task(task_entity.len)))
                res.set_answer(task_entity.tasks)
            elif task_entity.len == -1: 
                res.set_answer(task_entity.tasks)
                res.set_suggests([
                    {'title': 'Выйти', 'hide': True},
                    {'title': 'Создай проект Отдых', 'hide': True},
                    {'title': 'Создай проект Учеба', 'hide': True},
                ])
            else:
                res.set_answer("У вас нет просроченных задач, поздравляю!")
                res.set_suggests([
                    {'title': 'Выйти', 'hide': True},
                ])
            return
        elif req.recurring_task:
            project_name = req.get_project_name_recurring_task
            logging.info(f"project_name_for_task: {project_name}")

            non_reccuring = req.get_non_recurring

            task_entity = todoist.get_list_non_or_recurring_task(project_name = project_name, non_reccuring = non_reccuring)

            if(task_entity.len != 0):
                res.set_say_answer("У вас  {}".format(processing_task(task_entity.len)))
                res.set_answer(task_entity.tasks)
            elif task_entity.len == -1: 
                res.set_answer(task_entity.tasks)
                res.set_suggests([
                    {'title': 'Выйти', 'hide': True},
                    {'title': 'Создай проект Отдых', 'hide': True},
                    {'title': 'Создай проект Учеба', 'hide': True},
                ])
            else:
                res.set_answer("У вас нет задач, создадим задачу?")
                res.set_suggests([
                    {'title': 'Выйти', 'hide': True},
                    {'title': 'Добавь рыбу в покупки', 'hide': True},
                    {'title': 'Добавь практика языка в английский каждый день по 1 часу', 'hide': True},
                ])
            return
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
