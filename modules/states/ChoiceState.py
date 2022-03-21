from entities.AliceRequest import AliceRequest
from entities.AliceResponse import AliceResponse
from modules.context.Context import EXIT_WORDS
from modules.states.State import State


class ChoiceState(State):
    def handle_dialog(self, res: AliceResponse, req: AliceRequest):
        if set(req.words).intersection(EXIT_WORDS):
            res.set_answer('Пока!')
            res.end_session()
            return
        if req.access_token: 
            res.set_answer('Вы авторизированы!')
            return
        # if 'погода' in req.words or 'погоду' in req.words:
        #     self.context.transition_to(WeatherState())
        #     res.set_answer('Хорошо, пиши место, где надо узнать погоду!\n'
        #                    'Пиши: [место]')
        #     res.set_suggests([{'title': 'Погода в Москве', 'hide': True}])
        #     return
        # if 'карты' in req.words:
        #     self.context.transition_to(MapsState())
        #     res.set_answer('Введи любое место и я тебе его покажу на карте!')
        #     return
        res.set_answer('У нас есть несколько функций: переводчик, сканер, погода и карты.\n'
                       'Что хочешь попробовать?')
        res.set_suggests([{'title': 'Выйти', 'hide': True}])