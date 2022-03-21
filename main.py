import logging
from entities.AliceRequest import AliceRequest
from entities.AliceResponse import AliceResponse

from flask import Flask, request
from modules.context.Context import Context
from modules.states.HelloState import HelloState

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods=["POST"])

def main():
    logging.info(f"Req: {request.json}")

    alice_req = AliceRequest(request.json)
    alice_resp = AliceResponse(alice_req)

    answer = ""

    if alice_req.is_new_session:
        cnt = Context(HelloState())
        alice_resp._response["application_state"][alice_req.user_id] = cnt 
        #cnt.handle_dialog(alice_resp, alice_req)
        
        if alice_resp._response["application_state"].get(alice_req.user_id):
            answer = alice_req.user_id
        else: 
            answer = "пусто"
        alice_resp.set_answer(answer)
        logging.info(f"Resp: {alice_resp}")
        return alice_resp.to_json()
    

    #sessions[alice_req.user_id].handle_dialog(alice_resp, alice_req)
    if alice_resp._response["application_state"].get(alice_req.user_id):
        answer = alice_req.user_id
    else: 
        answer = "пусто"
    alice_resp.set_answer(answer)

    logging.info(f"Resp: {alice_resp}")
    
    return alice_resp.to_json()

















