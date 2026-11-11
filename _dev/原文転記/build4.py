# 練習問題④：t4a/t4b（原文転記）と q4exp（解説）と解答表から、
# index.html に入れる ORIG["4"]（原文）と Q4（出題データ）を作る。
# 使い方：python build4.py  → orig4.json と q4.js を出力
import json, re, sys
sys.path.insert(0, '.')
from t4b import T4
from q4exp import EXP, TOPIC
from buildorig_util import groups

ANS = '''問1: A1 B3 C1 D2 E3 F2 G2 H1 I3 J2
問2: A2 B4 C1 D11 E8
問3: A2 B5 C3 D5 E1 F6 G2 H4 I1 J4
問4: A3 B1 C2 D2 E1 F3 G3 H3 I2
問5: A2 B2 C2 D1 E1 F3 G1 H3
問6: A3 B3 C1 D2 E3 F2 G2 H3
問7: A1 B4 C5 D14 E12 F2 G11 H10
問8: A6 B2 C13 D12 E3 F8 G11 H7 I1 J5 K6
問9: A3 B2 C3 D1 E1 F3
問10: A1 B2 C1 D3 E2 F3
問11: A2 B2 C3 D3 E1 F2 G3 H1 I1 J2
問12: A1 B7 C4 D2 E2 F4 G3 H2 I7'''
A = {}
for line in ANS.splitlines():
    q, rest = line.split(':'); n = int(q[1:])
    A[f'q{n}'] = {m[0]: int(m[1:]) for m in rest.split()}
STAR = ['q7', 'q11', 'q12', 'q9', 'q6', 'q3', 'q10']   # 学びのポイント（問題集の表紙の順）

def opts_of(t):
    """para 型の各記号の選択肢（buildorig.py と同じ規則）"""
    opts = {}
    for s in t['secs']:
        lab, text, ks = s[0], s[1], s[2]
        gs = groups(text); used = set()
        blanks = [(m.start(), m.end(), m.group(1)) for m in re.finditer(r'\[([A-L])\]', text)]
        if not blanks:
            assert len(ks) == 1
            if gs: opts[ks] = gs[0][2]
        for (bs, be, k) in blanks:
            if k in opts: continue
            g = [x for x in gs if x[0] == be]
            if not g:
                g = [x for x in gs if x[0] > be and id(x) not in used and not any(b2[1] == x[0] for b2 in blanks)]
            if g: opts[k] = g[0][2]; used.add(id(g[0]))
    opts.update(t.get('opts', {}))
    return opts

def strip_groups(text):
    out = text
    for (a, b, _) in reversed(groups(text)):
        out = out[:a] + out[b:]
    return out

def item_x(text, k):
    """出題データ用の短い問題文：[k] を含む文（選択肢の括弧は除く）"""
    t = strip_groups(text).replace('\n', '')
    if '[' + k + ']' not in t:
        return t.strip()
    sents = re.split(r'(?<=。)', t)
    for s in sents:
        if '[' + k + ']' in s: return s.strip()
    return t.strip()

ORIG4 = {}; Q4 = []
for i in range(1, 13):
    qid = f'q{i}'; t = T4[qid]
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
    ORIG4[qid] = oq
    assert sorted(keys) == sorted(A[qid]), (qid, keys, A[qid])
    assert sorted(keys) == sorted(EXP[qid]), (qid, keys, sorted(EXP[qid]))
    q = {'id': qid, 't': f'問{i}', 'topic': TOPIC[qid]}
    if qid in STAR: q['star'] = True
    if t['type'] == 'para':
        q['type'] = 'own'; q['items'] = []
        for s in t['secs']:
            for k in s[2]:
                o = oq['opts'][k]; a = A[qid][k]; assert 1 <= a <= len(o), (qid, k, a, o)
                w, r = EXP[qid][k]
                q['items'].append({'k': k, 'x': item_x(s[1], k), 'o': o, 'a': a, 'w': w, 'r': r})
    else:
        q['type'] = 'shared'; q['sections'] = []
        for s in t['secs']:
            words = s[3]; sec = {'roman': s[0].replace('．', ''), 'stem': strip_groups(s[1]) if not s[1].startswith('{{') else '', 'words': words, 'items': []}
            for k in s[2]:
                a = A[qid][k]; assert 1 <= a <= len(words), (qid, k, a)
                w, r = EXP[qid][k]
                it = {'k': k, 'a': a, 'w': w, 'r': r}
                if 'itemx' in t: it['x'] = t['itemx'][k]
                sec['items'].append(it)
            q['sections'].append(sec)
    Q4.append(q)

n = sum(len(q.get('items') or [x for s in q['sections'] for x in s['items']]) for q in Q4)
json.dump(ORIG4, open('orig4.json', 'w', encoding='utf8'), ensure_ascii=False)
js = 'const Q4 = [\n' + ',\n'.join(json.dumps(q, ensure_ascii=False) for q in Q4) + '\n];\n'
open('q4.js', 'w', encoding='utf8').write(js)
print('items', n, 'stars', sum(1 for q in Q4 if q.get('star')))
