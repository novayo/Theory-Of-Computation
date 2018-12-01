import os
import requests


GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")


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
                    "image_url":"https://i.imgur.com/HekR9G2.png"
            },

            ]
        }
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response
"""
def send_template_mesg(id, title, image_url, subtitle, data):
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
                            "image_url": image_url,
                            "subtitle": subtitle,
                            "buttons": data
                        }
                    ]
                }
            }
        }
    }
"""
"""
def send_button_message(id, text, buttons):
    pass
"""
