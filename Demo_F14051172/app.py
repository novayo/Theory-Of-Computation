from bottle import route, run, request, abort, static_file

from fsm import TocMachine
VERIFY_TOKEN = "Messenger_Chatbot"
PORT = 2000

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
        machine.advance(event)
        return 'OK'
    

@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('F14051172-fsm.png', prog='dot', format='png')
    return static_file('F14051172-fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="localhost", port=PORT, debug=True) #, reloader=True