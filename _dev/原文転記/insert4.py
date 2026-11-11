# 練習問題④を index.html に組み込む（1回だけ実行する）。使い方：python insert4.py（_dev/原文転記 で実行）
import os
p = os.path.join('..', '..', 'index.html')
s = open(p, encoding='utf8').read()
assert 'const Q4 = [' not in s, 'すでに組み込み済み'
q4 = open('q4.js', encoding='utf8').read()
orig4 = open('orig4.json', encoding='utf8').read()
figs = open('figs4.js', encoding='utf8').read()

# 1) Q4 を原文データの直前に入れる
anchor = '// 問題集の原文（指示文・本文・選択肢・語群）'
assert s.count(anchor) == 1
s = s.replace(anchor, q4 + '\n' + anchor)

# 2) ORIG["4"] と、Q4 への原文の結び付け
old = '[Q1,Q2,Q3].forEach((qs,i)=>qs.forEach(q=>{ q.orig = ORIG[String(i+1)][q.id]; }));'
assert s.count(old) == 1
s = s.replace(old, 'ORIG["4"] = ' + orig4 + ';\n' + figs + '\n' + old.replace('[Q1,Q2,Q3]', '[Q1,Q2,Q3,Q4]'))

# 3) SETS に④を追加
old3 = "['q9','問9 編地特性・物性']]}\n];"
assert s.count(old3) == 1
s = s.replace(old3, "['q9','問9 編地特性・物性']]},\n"
  " {no:'④',name:'練習問題④',date:'2026年11月10日配布',Q:Q4,skey:'seni-renshu4-answers',\n"
  "  points:[['q7','問7 編物構造・編目'],['q11','問11 仕上加工'],['q12','問12 色管理・染色品質管理'],['q9','問9 物性・快適性能'],['q6','問6 物性管理・スナッグ'],['q3','問3 繊維物性'],['q10','問10 機能加工']]}\n];")

# 4) rich() で {{fig:名前}} を図に置き換える
BS = chr(92)
old4 = "replace(/" + BS + "n/g,'<br>'); }"
i = s.find('function rich(t)'); j = s.find(old4, i)
assert i > 0 and j > 0
new4 = "replace(/" + BS + "n/g,'<br>').replace(/" + BS + "{" + BS + "{fig:([" + BS + "w-]+)" + BS + "}" + BS + "}/g,(m,k)=>FIGS[k]||''); }"
s = s[:j] + new4 + s[j + len(old4):]

# 5) 図のスタイル
css_anchor = '.stem-wrap{position:sticky'
assert s.count(css_anchor) == 1
s = s.replace(css_anchor, '.fig{display:block;width:100%;max-width:560px;height:auto;margin:4px auto 8px;color:var(--ink)}\n' + css_anchor)

open(p, 'w', encoding='utf8').write(s)
print('ok')
