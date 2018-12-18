from bottle import route, run, request, abort, static_file
import redis
import os
from fsm import TocMachine
from utils import *
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
Port = int(os.environ['PORT'])

r = redis.from_url(os.environ["HEROKU_REDIS_SILVER_URL"])

machine = TocMachine(
    states=[
        'user',
        'state11',
        'state12',
        'state13',
        'state21',
        'state31',
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state11',
            'conditions': 'is_going_to_state11',
        },
        {
            'trigger': 'advance',
            'source': 'state11',
            'dest': 'state12',
            'conditions': 'is_going_to_state12',
        },
        {
            'trigger': 'advance',
            'source': 'state12',
            'dest': 'state13',
            'conditions': 'is_going_to_state13',
        },
                
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state21',
            'conditions': 'is_going_to_state21',
        },
                
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state31',
            'conditions': 'is_going_to_state31',
        },
        {
            'trigger': 'advance',
            'source':'state11',
            'dest': 'user',
        },

        {
            'trigger':'go_back',
            'source':[
                'state21',
                'state13',
                'state31',
            ],
            'dest':'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)

@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge
    else:
        abort(403)
 
@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        try:
            if r.get(event['sender']['id']) is None:
                r.set(event['sender']['id'], machine.state)
            machine.state = r.get(event['sender']['id']).decode("utf-8")
            machine.advance(event)
            r.set(event['sender']['id'], machine.state)
            return 'OK'
        except:
            responese = send_text_message(event['sender']['id'], "目前伺服器故障中，請稍後!")
            return 'OK'
            

@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('F14051172-fsm.png', prog='dot', format='png')
    return static_file('F14051172-fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="0.0.0.0", port=Port, debug=True, reloader=True) #, reloader=True