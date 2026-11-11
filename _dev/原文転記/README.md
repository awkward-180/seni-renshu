# 原文転記

練習問題①〜④の原文（指示文・本文・選択肢・語群）を書き写したデータ。

- `t1a.py`, `t1b.py`：練習問題①（T1）
- `t2a.py`, `t2b.py`：練習問題②（T2）
- `t3a.py`, `t3b.py`：練習問題③（T3）
- `t4a.py`, `t4b.py`：練習問題④（T4）。`q4exp.py` に解説とページ、`build4.py` に解答表がある。`python build4.py` で `orig4.json`（原文）と `q4.js`（出題データ）を作り、`insert4.py` で index.html に組み込んだ（組み込みは1回だけ。2026-11-11 実施）
- `figs4.js`：④問7の図（`fig/` の切り出し画像を並べる HTML）。index.html の `FIGS` と同じ
- `buildorig_util.py`：選択肢を取り出す関数（buildorig.py から抜き出したもの）
- `buildorig.py`：T1〜T3 から `orig.json` を作り、旧データ `old_data.json` の記号・選択肢と照合する（2026-11-06 の原文化で使用）
- `orig.json`：index.html の `ORIG` と同じ内容

現在は index.html 内の `ORIG` が正本。原文を直すときは index.html の `ORIG` を直接直してよい。
