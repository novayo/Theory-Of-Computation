from transitions.extensions import GraphMachine

from nlp import nlp
from utils import send_text_message, send_quick_reply, send_image_url, send_template_mesg

# 只能有一個方向
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def is_going_to_state11(self, event):
        if event.get("message"):
            # Try Except是為了分開收到文字還是貼圖
            try:
                text = nlp(event['message']['text'])
                for text_tmp in text:
                    if (text_tmp == '訂') or (text_tmp == '飲料') or (text_tmp == '菜餐') :
                        return True
                    
                sender_id = event['sender']['id']
                #responese = send_quick_reply(sender_id)
                #responese = send_image_url(sender_id, "https://i.imgur.com/HekR9G2.png")
                responese = send_template_mesg(sender_id, "飲料菜單", "請選擇","https://i.imgur.com/HekR9G2.png", [{'type': 'postback','title': "組合A",'payload': '娛樂新聞'},{'type': 'postback','title': "組合B",'payload': '體育新聞'},{'type': 'postback','title': "組合C",'payload': '雞腿bang當'}])
                #responese = send_text_message(sender_id, "請輸入\"我要訂飲料\"來觀看Menu!")
            except:
                sender_id = event['sender']['id']
                responese = send_text_message(sender_id, "請傳送文字11")
        
        return False

    def is_going_to_state12(self, event):
        if event.get("message"):
            try:
                text = event['message']['text']
                return text.lower() == 'go to state12'
            except:
                sender_id = event['sender']['id']
                responese = send_text_message(sender_id, "請傳送文字12")
        return False
    
    def is_going_to_state13(self, event):
        if event.get("message"):
            try:
                text = event['message']['text']
                return text.lower() == 'go to state13'
            except:
                sender_id = event['sender']['id']
                responese = send_text_message(sender_id, "請傳送文字13")
        return False
    
    def is_going_to_state21(self, event):
        if event.get("message"):
            try:
                text = event['message']['text']
                return text.lower() == 'go to state21'
            except:
                sender_id = event['sender']['id']
                responese = send_text_message(sender_id, "請傳送文字21")
        return False
    
    def is_going_to_state31(self, event):
        if event.get("message"):
            try:
                text = event['message']['text']
                return text.lower() == 'go to state31'
            except:
                sender_id = event['sender']['id']
                responese = send_text_message(sender_id, "請傳送文字31")
        return False
    
    def is_going_to_state32(self, event):
        if event.get("message"):
            try:
                text = event['message']['text']
                return text.lower() == 'go to state32'
            except:
                sender_id = event['sender']['id']
                responese = send_text_message(sender_id, "請傳送文字32")
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
