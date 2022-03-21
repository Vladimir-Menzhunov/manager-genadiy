from entities.AliceRequest import AliceRequest
from entities.AliceResponse import AliceResponse
from modules.alicecontext.AliceContext import YES_WORDS
from modules.alicestates.AliceState import AliceState


class AuthState(AliceState):
    def handle_dialog(self, res: AliceResponse, req: AliceRequest, todoist):
        if set(req.words).intersection(YES_WORDS):
            res.set_auth()
            res.set_str_state("ChoiceState")
        else: 
            res.set_answer('Пока!')
            res.end_session()


    def __str__(self):
        return "AuthState"

    def __repr__(self):
        return "AuthState"
