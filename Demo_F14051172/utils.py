import os
import requests


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
                    "title":"我要訂飲料",
                    "payload":"???",
                    #"image_url":"https://i.imgur.com/HekR9G2.png"
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

def send_receipt_mesg(id):
    payload = {
        "recipient": {"id": id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "receipt",
                    "recipient_name": "Stephane Crozatier",#
                    "order_number": "12345678902",#
                    "currency": "新台幣",
                    "payment_method": "貨到付款",
                    "order_url": "",
                    "timestamp": "1428444852",#
                    "address": {
                        "street_1": "No.1, Daxue Rd.",
                        "street_2": "East Dist.",
                        "city": "Tainan City",
                        "postal_code": "701",
                        "state": "Taiwan",
                        "country": "(R.O.C.)"
                    },
                            ###################################################
                    "summary": {
                        "subtotal": 75,
                        "shipping_cost": 4.95,
                        "total_tax": 6.19,
                        "total_cost": 56.14
                    },
                    "adjustments": 
                    [
                        {
                            "name": "New Customer Discount",
                            "amount": 20
                        },
                        {
                            "name": "$10 Off Coupon",
                            "amount": 10
                        }
                    ],
                    "elements": 
                    [
                        {
                            "title": "Classic White T-Shirt",
                            "subtitle": "100% Soft and Luxurious Cotton",
                            "quantity": 2,
                            "price": 50,
                            "currency": "USD",
                            "image_url": "http://petersapparel.parseapp.com/img/whiteshirt.png"
                        },
                        {
                            "title": "Classic Gray T-Shirt",
                            "subtitle": "100% Soft and Luxurious Cotton",
                            "quantity": 1,
                            "price": 25,
                            "currency": "USD",
                            "image_url": "http://petersapparel.parseapp.com/img/grayshirt.png"
                        }
                   ]
                } 
            }
        }
    }

"""
def send_button_message(id, text, buttons):
    pass
"""
