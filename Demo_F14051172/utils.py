import os
import requests
import time

GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")

# Finish
def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response


#Finish
def send_image_url(id, img_url):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": img_url
                }
            }
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response

#Finish
def send_quick_reply(id):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient":{"id":id},
        "message":{
            "text": "請點選下方按鈕開始 !",
            "quick_replies":[
            {
                    "content_type":"text",
                    "title":"點我訂飲料",
                    "payload":"???",
            },
            {
                    "content_type":"text",
                    "title":"點我加購",
                    "payload":"???",
            },
            {
                    "content_type":"text",
                    "title":"點我看訂單",
                    "payload":"???",
            },
            {
                    "content_type":"text",
                    "title":"離開",
                    "payload":"???",
            },

            ]
        }
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response

#Finish
"""
buttons = ([
        {'type': 'postback','title': "組合A",'payload': '娛樂新聞'},
        {'type': 'postback','title': "組合B",'payload': '體育新聞'},
        {'type': 'postback','title': "組合C",'payload': '雞腿bang當'},
 ])
"""
def send_template_mesg(id, title, subtitle, image_url, data):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id}, 
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": title,
                            "subtitle": subtitle,
                            "image_url": image_url,
                            "buttons": data,
                        }
                    ]
                }
            }
        }
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response

def send_receipt_mesg(id, name, order_number, payment_method, element):
    etmp = element
    price = 0
    for i in etmp:
        price += i["price"]
    ts = time.time()
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "receipt",
                    "recipient_name": name,#
                    "order_number": order_number,#
                    "currency": "TWD",
                    "payment_method": payment_method,
                    #"order_url": "",
                    "timestamp": int(ts),#
                    "address": {
                        "street_1": "東區大學路1號",
                        "street_2": "",
                        "city": "台南市",
                        "postal_code": "701",
                        "state": "台灣",
                        "country": "台灣"
                    },
                            ###################################################
                    "summary": {
                        "subtotal": price, #小計
                        "shipping_cost": 0, #手續費
                        "total_tax": 0, #稅金
                        "total_cost": price #總金額
                    },
                    "elements":element
                } 
            }
        }
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response

"""
def send_button_message(id, text, buttons):
    pass
"""
