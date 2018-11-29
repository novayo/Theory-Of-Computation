from bottle import route, run, request, abort, static_file

from fsm import TocMachine
PORT = 2002

VERIFY_TOKEN = "Messenger_Chatbot"

machine = TocMachine(
    states=[
        'user',
        'state11',
        'state12',
        'state13',
        'state21',
        'state31',
        'state32',
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
            'source': 'state31',
            'dest': 'state32',
            'conditions': 'is_going_to_state32',
        },        
        
        {
            'trigger': 'go_back',
            'source': [
                'state13',
                'state21',
                'state32',
            ],
            'dest': 'user',
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)

'''
# state只能是state開頭
machine = TocMachine(
    states=[
        'user',
        'state1',
        'state2',
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state1',
            'conditions': 'is_going_to_state1',
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state2',
            'conditions': 'is_going_to_state2',
        },
        {
            'trigger': 'go_back',
            'source': [
                'state1',
                'state2',
            ],
            'dest': 'user',
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)
'''

@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge
    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('----------------------------------------------------------------------')
    print('\nFSM STATE: ' + machine.state)
    print('\nREQUEST BODY: ')
    print(body)
    

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        # nlp
        machine.advance(event)
        return 'OK'
    

@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('my_fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./img/', mimetype='image/png')


if __name__ == "__main__":
    run(host="localhost", port=PORT, debug=True) #, reloader=True