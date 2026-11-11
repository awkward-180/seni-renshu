# buildorig.py と同じ「（1．…）」の選択肢を取り出す関数
import re
def groups(text):
    out=[];i=0
    while True:
        j=text.find('（1．',i)
        if j<0: break
        d=0;k=j
        while k<len(text):
            if text[k]=='（': d+=1
            elif text[k]=='）':
                d-=1
                if d==0: break
            k+=1
        inner=text[j+1:k]
        parts=[p.strip(' 　\n') for p in re.split(r'(?:^|[\s　\n]+)\d{1,2}．',inner) if p.strip(' 　\n')]
        out.append((j,k+1,parts)); i=k+1
    return out
