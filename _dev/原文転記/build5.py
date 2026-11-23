# 練習問題⑤：t5a/t5b（原文転記）と q5exp（解説）と解答表から、
# index.html に入れる ORIG["5"]（原文）と Q5（出題データ）を作る。
# 使い方：python build5.py  → orig5.json と q5.js を出力
import json, re, sys
sys.path.insert(0, '.')
from t5b import T5
from q5exp import EXP, TOPIC
from build4 import opts_of, strip_groups, item_x   # ④と同じ規則（import 時に build4 も実行されるが出力は同じ）

ANS = '''問1: A2 B3 C2 D3 E3 F1 G3 H1 I2 J1 K1 L2
問2: A5 B2 C1 D3 E6
問3: A2 B1 C3 D2 E1 F2 G2 H3
問4: A2 B1 C1 D3 E1 F2 G1 H2 I1 J3
問5: A2 B1 C2 D1 E1 F1 G3 H2 I1 J1
問6: A2 B3 C1 D3 E2 F2 G1 H1
問7: A7 B9 C6 D13
問8: A3 B5 C19 D9 E20 F10 G14 H17 I11
問9: A5 B3 C7 D9 E8 F7 G3 H4 I1
問10: A2 B1 C1 D2 E3 F3 G2
問11: A3 B2 C3 D1 E1 F2 G3 H2 I2 J1
問12: A4 B2 C1 D3 E8 F4 G11 H12'''
ALL = {('q11', 'D')}   # 解答表「問11-Dは設問の内容に不備があったため全員正解扱い」
A = {}
for line in ANS.splitlines():
    q, rest = line.split(':'); n = int(q[1:])
    A[f'q{n}'] = {m[0]: int(m[1:]) for m in rest.split()}
STAR = ['q6', 'q7', 'q10', 'q11', 'q12', 'q2', 'q1']   # 学びのポイント（問題集の表紙の順）
TF3 = ['①②とも正しい', '①②のいずれかが誤り', '①②とも誤り']

def plain(s):
    return re.sub(r'<[^>]+>', '', s)

ORIG5 = {}; Q5 = []
for i in range(1, 13):
    qid = f'q{i}'; t = T5[qid]
    q = {'id': qid, 't': f'問{i}', 'topic': TOPIC[qid]}
    if qid in STAR: q['star'] = True
    if t['type'] == 'tf':
        ORIG5[qid] = {'ins': t['ins'], 'type': 'tf', 'tf3': True, 'tf': {k: list(v) for k, v in t['tf'].items()}}
        q['type'] = 'tf'; q['items'] = []
        assert sorted(t['tf']) == sorted(A[qid]) == sorted(EXP[qid])
        for k, (s,) in t['tf'].items():
            v1, v2, r = EXP[qid][k]; a = A[qid][k]
            bad = (not v1[0]) + (not v2[0]); assert a == 1 + bad, (qid, k, a, bad)   # 解答と①②の正誤が合っているか
            q['items'].append({'k': k, 'x': plain(s), 'a': a, 'v1': list(v1), 'v2': list(v2), 'r': r})
        Q5.append(q); continue
    oq = {'ins': t['ins'], 'type': t['type'], 'bl': t.get('bl', ''), 'html': bool(t.get('html'))}
    secs = []; keys = []
    for s in t['secs']:
        sd = {'lab': s[0], 'text': s[1], 'keys': list(s[2])}
        if len(s) > 3: sd['words'] = s[3]
        secs.append(sd); keys += list(s[2])
    oq['secs'] = secs
    oq['opts'] = opts_of(t) if t['type'] == 'para' else {}
    if 'itemx' in t: oq['itemx'] = t['itemx']
    if t.get('nolab'): oq['nolab'] = True
    if t['type'] == 'shared': oq['wl'] = '［語群］'
    ORIG5[qid] = oq
    assert sorted(keys) == sorted(A[qid]), (qid, keys, A[qid])
    assert sorted(keys) == sorted(EXP[qid]), (qid, keys, sorted(EXP[qid]))
    if t['type'] == 'para':
        q['type'] = 'own'; q['items'] = []
        for s in t['secs']:
            for k in s[2]:
                o = oq['opts'][k]; a = A[qid][k]; assert 1 <= a <= len(o), (qid, k, a, o)
                w, r = EXP[qid][k]
                it = {'k': k, 'x': plain(item_x(s[1], k)), 'o': o, 'a': a, 'w': w, 'r': r}
                if (qid, k) in ALL: it['all'] = True
                q['items'].append(it)
    else:
        q['type'] = 'shared'; q['sections'] = []
        for s in t['secs']:
            words = s[3]
            stem = '' if s[1].startswith('{{') or s[1].startswith('<table') else plain(strip_groups(s[1])).split('{{')[0].strip()
            sec = {'roman': s[0].replace('．', ''), 'stem': stem, 'words': words, 'items': []}
            for k in s[2]:
                a = A[qid][k]; assert 1 <= a <= len(words), (qid, k, a)
                w, r = EXP[qid][k]
                it = {'k': k, 'a': a, 'w': w, 'r': r}
                if 'itemx' in t: it['x'] = t['itemx'][k]
                sec['items'].append(it)
            q['sections'].append(sec)
    Q5.append(q)

n = sum(len(q.get('items') or [x for s in q['sections'] for x in s['items']]) for q in Q5)
json.dump(ORIG5, open('orig5.json', 'w', encoding='utf8'), ensure_ascii=False)
js = 'const Q5 = [\n' + ',\n'.join(json.dumps(q, ensure_ascii=False) for q in Q5) + '\n];\n'
open('q5.js', 'w', encoding='utf8').write(js)
print('items', n, 'stars', sum(1 for q in Q5 if q.get('star')))
