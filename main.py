import logging
from entities.AliceRequest import AliceRequest
from entities.AliceResponse import AliceResponse

from flask import Flask, request
from entities.AliceTodoist import AliceTodoist

from modules.alicecontext.AliceContext import AliceContext
from modules.alicestates.AuthState import AuthState
from modules.alicestates.ChoiceState import ChoiceState
from modules.alicestates.HelloState import HelloState


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods=["POST"])

def main():

    logging.info(f"Req: {request.json}")

    alice_req = AliceRequest(request.json)
    
    alice_todoist = None
    if(alice_req.access_token):
        alice_todoist = AliceTodoist(alice_req)

    state = get_current_state(alice_req)   
    logging.info(f"State: {state}")

    alice_resp = AliceResponse(alice_req, state)
    
    alice_resp.get_application_state().handle_dialog(alice_resp, alice_req, alice_todoist)

    logging.info(f"Resp: {alice_resp}")
    
    return alice_resp.to_json()

def get_current_state(alice_req: AliceRequest):
    current_state = "HelloState"
            
    if alice_req.state_application != {}:
        current_state = str(alice_req.state_application[alice_req.user_id])

    dictState = {
        "ChoiceState": AliceContext(ChoiceState()),
        "HelloState": AliceContext(HelloState()),
        "AuthState": AliceContext(AuthState())
    }
        
    logging.info(f"get_current_state: {current_state}")
    

    return dictState[current_state]














