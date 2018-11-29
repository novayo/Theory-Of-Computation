from transitions.extensions import GraphMachine

from utils import send_text_message

# 只能有一個方向
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def is_going_to_state11(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'go to state11' # 使用者打的字
        return False

    def is_going_to_state12(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'go to state12'
        return False
    
    def is_going_to_state13(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'go to state13'
        return False
    
    def is_going_to_state21(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'go to state21'
        return False
    
    def is_going_to_state31(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'go to state31'
        return False
    
    def is_going_to_state32(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'go to state32'
        return False




    def on_enter_state11(self, event):
        print("I'm entering state11")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "I'm entering state11")

    def on_enter_state12(self, event):
        print("I'm entering state12")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "I'm entering state12")

    def on_enter_state13(self, event):
        print("I'm entering state13")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "I'm entering state13")
        self.go_back()
        
    def on_enter_state21(self, event):
        print("I'm entering state21")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "I'm entering state21")
        self.go_back()

    def on_enter_state31(self, event):
        print("I'm entering state31")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "I'm entering state31")
    
    def on_enter_state32(self, event):
        print("I'm entering state32")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "I'm entering state32")
        self.go_back()


    def on_exit_state11(self, event):
        print('Leaving state11')    
        
    def on_exit_state12(self, event):
        print('Leaving state12')    
        
    def on_exit_state13(self):
        print('Leaving state13')

    def on_exit_state21(self):
        print('Leaving state21')
    
    def on_exit_state31(self, event):
        print('Leaving state31')

    def on_exit_state32(self):
        print('Leaving state32')
