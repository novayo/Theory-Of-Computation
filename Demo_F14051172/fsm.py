from transitions.extensions import GraphMachine

import json
import codecs
from my_utils import *
from utils import *

# 只能有一個方向
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )
        
        with codecs.open('data.json', 'r', 'utf-8') as file:
            file.text = file.read()
        self.data = json.loads(file.text)
        self.type = ['title', 'quantity', 'subtitle']
        self.if_first_in = 1
        self.if_see_menu = 0
        self.if_ordered = 0
        self.tmp_order = []

    def initial_all_vars(self):
        self.if_first_in = 1
        self.if_ordered = 0
        self.if_see_menu = 0
        self.tmp_order = []
        
        
    def is_going_to_state11(self, event):
        if event.get("message"):
            # Try Except是為了分開收到文字還是貼圖
            try:
                text = nlp(event['message']['text'])
                for text_tmp in text:
                    if (text_tmp == '訂') or (text_tmp == '飲料'): #or (self.if_ordered == 1 and ((text_tmp == '加購') or (text_tmp == '加訂') or (text_tmp == '加'))) :
                        self.if_first_in = 0
                        return True
                    elif (text_tmp == '點我寫') or (text_tmp == '評論') or (text_tmp == '看菜') or (text_tmp == '單'):
                        return False
   
                if self.if_first_in == 1:
                    responese = send_quick_reply(event['sender']['id']) #選 "訂飲料" "加購" "看訂單"
                    return False
            except:
                responese = send_text_message(event['sender']['id'], "請輸入文字")
        
        return False

    def is_going_to_state12(self, event):
        if event.get("message"):
            #判斷是否輸入格式正確與否
            try:
                text = event['message']['text']
                #若找到空格(則輸入了收件人了)
                if (self.if_ordered == 1) and (text.find(' ') != -1):
                    tmptext = text.split(' ', 1)
                    k=0
                    for t in tmptext:
                        if (k == 1) and (t != '到店取餐'): 
                            responese = send_text_message(event['sender']['id'], "我們目前沒有外送服務喔! 取餐地點請看訂單資訊!")
                            t = '到店取餐'
                        self.tmp_order.append(t)
                        k+=1
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
                        if j==2: dtmp['subtitle'] = ""
                        dtmp['price'] = int(dtmp['quantity']) * int(self.data[which_drink]['price'])
                        dtmp['image_url'] = self.data[which_drink]['image_url']
                        dtmp['currency'] = 'TWD'
                        self.tmp_order.append(dtmp)
                    
                        responese = send_text_message(event['sender']['id'], "請繼續以相同格式輸入您的訂單!\n若想結束請以以下格式回復 : \n\n收件人 到店取餐")
                        return False
                    responese = send_text_message(event['sender']['id'], "請輸入正確格式!")
            except:
                responese = send_text_message(event['sender']['id'], "請傳送文字12")
        return False
    
    def is_going_to_state13(self, event):
        if event.get("postback"):
            try:
                text = event['postback']['payload']
                if text == '我已取餐並付款':
                    return seller_check()
                responese = send_text_message(event['sender']['id'], "請等待叫號喔!!")
            except:
                responese = send_text_message(event['sender']['id'], "請傳送文字13")
        return False
    
    def is_going_to_state21(self, event):
        if event.get("message"):
            try:
                text = nlp(event['message']['text'])
                for text_tmp in text:
                    if (text_tmp == '單') or (text_tmp == '看菜'):
                        responese = send_image_url(event['sender']['id'], "http://bit.ly/菜單-F14051172")
                        self.if_see_menu = 1
                        return True
            except:
                return False
        return False
    
    def is_going_to_state31(self, event):
        if event.get("message"):
            try:
                text = nlp(event['message']['text'])
                for text_tmp in text:
                    if (text_tmp == '評論') or (text_tmp == '點我寫'):
                        return True
            except:
                return False
        return False



    def on_enter_state11(self, event):
        if self.if_see_menu == 0: 
            responese = send_image_url(event['sender']['id'], "http://bit.ly/菜單-F14051172")
            self.if_see_menu = 1
        responese = send_text_message(event['sender']['id'], "請以以下格式回復 : \n飲料/杯數/附註\n\n\n[附註若未標示糖冰則以正常糖冰為主!]")
        
    def on_enter_state12(self, event):
        responese = send_text_message(event['sender']['id'], "訂單形成中請稍後...")
        responese = send_receipt_mesg(event['sender']['id'], self.tmp_order[-2], "001", self.tmp_order[-1], self.tmp_order[:len(self.tmp_order)-2])
        responese = send_button_message(event['sender']['id'], "確認取餐", [{"type":"postback","title":"我已取餐並付款","payload":"我已取餐並付款"}])

    def on_enter_state13(self, event):
        responese = send_text_message(event['sender']['id'], "交易完成，謝謝您的惠顧，歡迎再次光臨!")
        self.initial_all_vars()
        self.go_back()
        
    def on_enter_state21(self, event):
        responese = send_text_message(event['sender']['id'], "輸入任意文字以繼續...")
        self.go_back()
        
    def on_enter_state31(self, event):
        responese = send_button_message(event['sender']['id'], "歡迎評論!", [{"type":"web_url","url":"https://www.facebook.com/pg/線上訂購飲料平台-1986065674805738/reviews/","title":"點我寫評論","webview_height_ratio": "full"}])
        self.initial_all_vars()
        self.go_back()


    def on_exit_state11(self,event):
        print('Leaving state11')    
        
    def on_exit_state12(self, event):
        print('Leaving state12')    
        
    def on_exit_state13(self):
        print('Leaving state13')

    def on_exit_state21(self):
        print('Leaving state21')
    
    def on_exit_state31(self):
        print('Leaving state31')


