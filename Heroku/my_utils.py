import jieba
import time

def nlp(text):
    seg_msg = jieba.cut(text)
    s = []
    
    # list 切割之後會有問題
    for i in seg_msg:
        s.append(i)
        print(i)

    return s

def find_slash(text):
    slash1 = text.find('/', 0)
    if slash1 == -1: #找不到
        return -1
    slash2 = text.find('/', slash1+1)
    if slash2 == -1:
        return 1
    
    return 2

def seller_check():
    #有機會設計一個假的server來確認買家有來領東西
    time.sleep(5)
    return True