from transitions.extensions import GraphMachine

import json
import codecs
from my_utils import nlp, find_slash
from utils import send_text_message, send_quick_reply, send_image_url, send_template_mesg, send_receipt_mesg

# 只能有一個方向
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )
        
        ###############################################歸零還沒想
        with codecs.open('data.json', 'r', 'utf-8') as file:
            file.text = file.read()
        self.data = json.loads(file.text)
        
        self.type = ['title', 'quantity', 'subtitle']
        self.if_first_in = 1
        self.end = 0
        self.tmp_order = []
        self.if_ordered = 0  

    def is_going_to_state11(self, event):
        if event.get("message"):
            # Try Except是為了分開收到文字還是貼圖
            try:
                text = nlp(event['message']['text'])
                for text_tmp in text:
                    if (text_tmp == '訂') or (text_tmp == '飲料') or (text_tmp == '單'): #or (self.if_ordered == 1 and ((text_tmp == '加購') or (text_tmp == '加訂') or (text_tmp == '加'))) :
                        self.if_first_in = 0
                        return True
                    elif text_tmp == '離開':
                        self.if_first_in = 1
                        self.end = 1
                        sender_id = event['sender']['id']
                        responese = send_text_message(sender_id, "謝謝您的惠顧!")
                        return True
   
                if self.if_first_in == 1:
                    sender_id = event['sender']['id']
                    responese = send_quick_reply(sender_id) #選 "訂飲料" "加購" "看訂單" "離開"
                    return False
              
                '''
                responese = send_receipt_mesg(sender_id, "李祁恬", "001", "到店付款", 
                    [
                        {
                            "title": "珍珠奶茶", #名稱
                            "subtitle": "半糖少冰", #糖冰
                            "quantity": 1, # 數量
                            "price": 50, 
                            "currency": "TWD",
                            #"image_url": "https://i.imgur.com/mgBWa5P.png"
                        },
                        {
                            "title": "熱可可",
                            "subtitle": "加袋子",
                            "quantity": 1,
                            "price": 49,
                            "currency": "TWD",
                            #"image_url": "https://i.imgur.com/HekR9G2.png"
                        }
                   ])
    '''
                #responese = send_image_url(sender_id, "https://i.imgur.com/J7S4zJ5.png")
                #responese = send_template_mesg(sender_id, "飲料菜單", "請選擇","https://i.imgur.com/HekR9G2.png", [{'type': 'postback','title': "組合A",'payload': '娛樂新聞'},{'type': 'postback','title': "組合B",'payload': '體育新聞'},{'type': 'postback','title': "組合C",'payload': '雞腿bang當'}])
                #responese = send_text_message(sender_id, "請輸入\"我要訂飲料\"來觀看Menu!")
            except:
                sender_id = event['sender']['id']
                responese = send_text_message(sender_id, "請傳送文字11")
        
        return False

    def is_going_to_state12(self, event):
        if event.get("message"):
            #判斷是否輸入格式正確與否
            try:
                text = event['message']['text']
                
                #若找到空格(則輸入了收件人了)
                if (self.if_ordered == 1) and (text.find(' ') != -1):
                    tmptext = text.split(' ', 1)
                    for t in tmptext:
                        self.tmp_order.append(t)
                    return True
                else:
                    #先確認是否有1個或2個/
                    text_split = find_slash(text)
                    if text_split == -1:
                        responese = send_text_message(event['sender']['id'], "格式錯誤!\n請重新輸入這筆資料!")
                        return False #go_back()
                    else:
                        self.if_ordered = 1
                        dtmp = {}
                        tmptext = text.split('/', text_split)
                        j = 0
                        which_drink = -1
                        print('1'*30)
                        for t in tmptext:
                            print(t)
                            if (self.type[j] == 'title'): 
                                b = next((i for i,x in enumerate(self.data) if x[self.type[j]] == t), -1)
                                if (b != -1): #輸入的沒有錯
                                    dtmp[self.type[j]] = t
                                    which_drink = b
                                else:
                                    responese = send_text_message(event['sender']['id'], "品項錯誤!\n請重新輸入這筆資料!")
                                    return False
                            else:
                                dtmp[self.type[j]] = t
                            j+=1
                            print('2'*30)
                        if j==2: dtmp['subtitle'] = ""
                        dtmp['price'] = int(dtmp['quantity']) * int(self.data[which_drink]['price'])
                        dtmp['image_url'] = self.data[which_drink]['image_url']
                        dtmp['currency'] = 'TWD'
                        print('3'*30)
                        self.tmp_order.append(dtmp)
                    
                        sender_id = event['sender']['id']
                        responese = send_text_message(sender_id, "請繼續以相同格式輸入您的訂單!\n\n\n若想結束請以以下格式回復 : \n\n收件人 [到店付款 或是 外送]")
                        return False
                    sender_id = event['sender']['id']
                    responese = send_text_message(sender_id, "請輸入正確格式!")

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
                text = nlp(event['message']['text'])
                for text_tmp in text:
                    if (text_tmp == '加購') or (text_tmp == '加訂') or (text_tmp == '加') :
                        #self.if_first_in = 0
                        #self.if_ordered = 1
                        return True
            except:
                sender_id = event['sender']['id']
                responese = send_text_message(sender_id, "請傳送文字21")
        return False
    
    def is_going_to_state22(self, event):
        if True: # 確認是否已經有訂單
            #self.if_ordered = 1
            return True 
        else:
            #self.if_ordered = 0
            return False
    
    def is_going_to_state31(self, event):
        if event.get("message"):
            try:
                text = nlp(event['message']['text'])
                for text_tmp in text:
                    if (text_tmp == '看訂單') or (text_tmp == '訂單') or (text_tmp == '確認') or (text_tmp == '確認訂單') :
                        self.if_first_in = 0
                        return True
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
        if self.end == 1:
            self.end = 0
            self.go_back()
        else:
            print("show Menu")
    
            sender_id = event['sender']['id']
            responese = send_text_message(sender_id, "請以以下格式回復 : \n\n飲料/杯數/附註\n\n\n[附註若未標示糖冰則以正常糖冰為主!]")
            responese = send_image_url(sender_id, "http://bit.ly/菜單-F14051172")

    def on_enter_state12(self, event):
        print("I'm entering state12")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "訂單形成中請稍後...")
        
        responese = send_receipt_mesg(sender_id, self.tmp_order[-2], "001", self.tmp_order[-1], 
                                      self.tmp_order[:len(self.tmp_order)-2])

        

    def on_enter_state13(self, event):
        print("I'm entering state13")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "I'm entering state13")
        self.if_first_in = 1
        self.go_back()
        
    def on_enter_state21(self, event):
        print("I'm entering state21")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "I'm entering state21")
    
    def on_enter_state22(self, event):
        print("I'm entering state21")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "I'm entering state11")
        
    def on_enter_state31(self, event):
        print("I'm entering state31")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "I'm entering state31")
    
    def on_enter_state32(self, event):
        print("I'm entering state32")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "I'm entering state32")
        self.if_first_in = 1
        self.go_back()


    def on_exit_state11(self,event):
        print('Leaving state11')    
        
    def on_exit_state12(self, event):
        print('Leaving state12')    
        
    def on_exit_state13(self):
        print('Leaving state13')

    def on_exit_state21(self, event):
        print('Leaving state21')
    
    def on_exit_state22(self, event):
        print('Leaving state22')
    
    def on_exit_state31(self, event):
        print('Leaving state31')

    def on_exit_state32(self):
        print('Leaving state32')
