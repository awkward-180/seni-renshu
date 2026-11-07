// スマホ幅（375px）での表示確認。使い方：node _dev/テスト/check.mjs [問題集番号]
// 事前に `npm i -D playwright` と `npx playwright install chromium` が必要。
import { chromium } from 'playwright';
import path from 'path';
import { pathToFileURL } from 'url';
const set = process.argv[2] || '1';
const file = pathToFileURL(path.resolve('index.html')).href + '?set=' + set;
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 375, height: 740 } });
const errs = []; p.on('pageerror', e => errs.push(e.message));
await p.route(/googletagmanager|fonts\.g/, r => r.fulfill({ body: '', contentType: 'text/css' }));
await p.goto(file);
// 大問1の最初の小問に答えてみる（語群・選択肢どちらの形式でも最初のボタン）
const btn = await p.$('section.q button.chip');
if (btn) await btn.click();
const res = await p.evaluate(() => ({
  pageWidth: document.documentElement.scrollWidth,
  wideTables: [...document.querySelectorAll('#result .tbl')].filter(t => t.scrollWidth > t.clientWidth).length,
  score: document.querySelector('#result .big b')?.textContent,
}));
console.log('ページ幅（375 ならはみ出しなし）:', res.pageWidth);
console.log('はみ出している得点表の数:', res.wideTables);
console.log('平均点の表示:', res.score);
console.log('エラー:', errs.length ? errs : 'なし');
await p.screenshot({ path: 'check.png', fullPage: false });
await b.close();
