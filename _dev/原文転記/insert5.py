# 練習問題⑤を index.html に組み込む（1回だけ実行する）。使い方：python insert5.py（_dev/原文転記 で実行）
# ⑤で新しく必要になった表示：
#  - 問6：選択肢3つの正誤問題（tf3）。下線部を <u> で示した1文で出題する
#  - 問11-D：全員正解扱い（小問に all:true）。どれを選んでも正解になる
#  - 問8：左寄せの表（otbl tl）、問7：4つ並びの図（figset f4）
import os
p = os.path.join('..', '..', 'index.html')
s = open(p, encoding='utf8').read()
assert 'const Q5 = [' not in s, 'すでに組み込み済み'
q5 = open('q5.js', encoding='utf8').read()
orig5 = open('orig5.json', encoding='utf8').read()
figs = open('figs5.js', encoding='utf8').read()

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (old, s.count(old))
    s = s.replace(old, new)

# 1) Q5 を原文データの直前に入れる
anchor = '// 問題集の原文（指示文・本文・選択肢・語群）'
rep(anchor, q5 + '\n' + anchor)

# 2) ORIG["5"]・図と、Q5 への原文の結び付け
old = '[Q1,Q2,Q3,Q4].forEach((qs,i)=>qs.forEach(q=>{ q.orig = ORIG[String(i+1)][q.id]; }));'
rep(old, 'ORIG["5"] = ' + orig5 + ';\n' + figs + '\n' + old.replace('[Q1,Q2,Q3,Q4]', '[Q1,Q2,Q3,Q4,Q5]'))

# 3) SETS に⑤を追加
old3 = "['q3','問3 繊維物性'],['q10','問10 機能加工']]}\n];"
rep(old3, "['q3','問3 繊維物性'],['q10','問10 機能加工']]},\n"
  " {no:'⑤',name:'練習問題⑤',date:'2026年11月20日配布',Q:Q5,skey:'seni-renshu5-answers',\n"
  "  points:[['q6','問6 編物基礎'],['q7','問7 編組織'],['q10','問10 仕上加工・機能加工'],['q11','問11 染色加工'],['q12','問12 漂白・色管理'],['q2','問2 物性管理'],['q1','問1 繊維特性・極細繊維']]}\n];")

# 4) 正誤の判定を OK(it,c) にまとめる（全員正解扱いの小問のため）
rep("const TF = ['①②とも正しい','①正 ②誤','①誤 ②正','①②とも誤り'];",
    "const TF = ['①②とも正しい','①正 ②誤','①誤 ②正','①②とも誤り'];\n"
    "const TF3 = ['①②とも正しい','①②のいずれかが誤り','①②とも誤り'];   // ⑤問6（選択肢3つ）\n"
    "// 正解かどうか。all:true の小問（⑤問11-D：設問の不備で全員正解扱い）はどれを選んでも正解\n"
    "const OK = (it,c) => c!=null && (it.all ? true : c===it.a);")
rep("if(c!=null){ done++; if(c===it.a) ok++; }", "if(c!=null){ done++; if(OK(it,c)) ok++; }", 2)
rep("if(c!=null){done++; if(c===it.a) ok++;}", "if(c!=null){done++; if(OK(it,c)) ok++;}")
s = s.replace("state[keyOf(q,it.k)]===it.a", "OK(it,state[keyOf(q,it.k)])")
rep("return c==null?true:c===it.a;", "return c==null?true:OK(it,c);")
rep("if(shown && n===it.a) cls+=' right';\n    else if(ch===n && n!==it.a) cls+=' wrong';",
    "if(shown && (it.all || n===it.a)) cls+=' right';\n    else if(ch===n && !OK(it,n)) cls+=' wrong';")
rep("return ch===it.a ? '<span class=\"verdict ok\">正解</span>'", "return OK(it,ch) ? '<span class=\"verdict ok\">正解</span>'")
rep("<b>正解 ${it.a}　${rich(optText)}</b>",
    "<b>正解 ${it.all ? (it.o||[]).map((_,i)=>i+1).join('・')+'（全員正解扱い）' : it.a+'　'+rich(optText)}</b>")

# 5) 選択肢3つの正誤問題（tf3）と、下線つき1文の出題
rep("return `<div class=\"ex\">${verdict(q,it)} <b>正解 ${it.a}</b>（${TF[it.a-1]}）",
    "return `<div class=\"ex\">${verdict(q,it)} <b>正解 ${it.a}</b>（${(q.orig&&q.orig.tf3?TF3:TF)[it.a-1]}）")
old5 = ("return Object.keys(o.tf).map(k=>{const it=byK[k],[a,b]=o.tf[k];\n"
        "      return `<div class=\"item\"><div class=\"stmts\"><div class=\"stmt\"><span class=\"lab\">${k}．</span><span>①${rich(a)}</span></div><div class=\"stmt\"><span></span><span>②${rich(b)}</span></div></div>${chipHTML(q,it,TF,false)}${exHTML(q,it)}</div>`;}).join('');")
new5 = ("const T=o.tf3?TF3:TF;\n"
        "    return Object.keys(o.tf).map(k=>{const it=byK[k],[a,b]=o.tf[k];\n"
        "      const st = b==null ? `<div class=\"stmt\"><span class=\"lab\">${k}．</span><span>${rich(a)}</span></div>` : `<div class=\"stmt\"><span class=\"lab\">${k}．</span><span>①${rich(a)}</span></div><div class=\"stmt\"><span></span><span>②${rich(b)}</span></div>`;\n"
        "      return `<div class=\"item\"><div class=\"stmts\">${st}</div>${chipHTML(q,it,T,false)}${exHTML(q,it)}</div>`;}).join('');")
rep(old5, new5)

# 6) rich()：<u>（下線）と左寄せの表を通す
rep("replace(/&lt;(\\/?)(sub|sup|tr|th|td)( colspan=", "replace(/&lt;(\\/?)(sub|sup|tr|th|td|u)( colspan=")
rep("replace(/&lt;table class=&quot;otbl&quot;&gt;/g,'<table class=\"otbl\">')",
    "replace(/&lt;table class=&quot;otbl( tl)?&quot;&gt;/g,(m,t)=>'<table class=\"otbl'+(t||'')+'\">')")

# 7) スタイル：左寄せの表、4つ並びの図、下線
css_anchor = '.stem-wrap{position:sticky'
rep(css_anchor,
    '.otbl.tl td{text-align:left}.otbl.tl th{white-space:nowrap;width:4.5em}\n'
    '.figset.f4{grid-template-columns:repeat(4,minmax(0,1fr));max-width:720px}\n'
    '@media (max-width:560px){.figset.f4{grid-template-columns:1fr 1fr}.figset.f4 figure:nth-child(3){grid-column:auto;justify-self:stretch;width:auto}}\n'
    '.stmt u{text-underline-offset:3px}\n' + css_anchor)

# 8) 1枚だけの図（⑤問9）：画面幅に合わせ、問題文の枠で切れないようにする（2026-11-24 確認時に追加）
rep('.stem-wrap .stem:has(.figset){', 'img.fig{display:block;width:100%;max-width:560px;height:auto;margin:6px auto 4px;background:#fff;border-radius:6px}
.stem-wrap .stem:has(.figset),.stem-wrap .stem:has(img.fig){')

open(p, 'w', encoding='utf8').write(s)
print('ok')
