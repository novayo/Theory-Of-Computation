import jieba

def nlp(text):
    seg_msg = jieba.cut(text)
    s = []
    
    # list 切割之後會有問題
    for i in seg_msg:
        s.append(i)
        print(i)

    return s