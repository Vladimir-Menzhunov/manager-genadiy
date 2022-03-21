from entities.AliceRequest import AliceRequest
from entities.AliceResponse import AliceResponse
from modules.states.ChoiceState import ChoiceState
from modules.states.State import State

class HelloState(State):
    def handle_dialog(self, res: AliceResponse, req: AliceRequest):
        res.set_answer('Привет. Меня зовут Алиса.\nА это новый мультинавык от разрабов МВД')
        self.context.transition_to(ChoiceState())