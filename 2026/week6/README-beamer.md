# 第6回スライド（Beamer版）

[2025年度の第6回PDF](../../2025/week6/week6.pdf)と[実習ノートブック](../../2025/week6/week6.ipynb)を元に、[共通テンプレート](../../templates/beamer/README.md)で作成しています。講義日は2026年11月24日、著者は野垣 康介、藤本 悠輝の順です。

- [編集用スライド](slide.tex)
- [配布用PDF](slide.pdf)
- [実習ノートブック](week6.ipynb)
- [図の再生成スクリプト](make_figures.py)
- `figures/`: 数値微分の誤差グラフ

表紙1枚と本文20枚の計21ページです。浮動小数点数、情報落ち・桁落ち、前進差分・後退差分・中心差分、二階微分の中心差分、刻み幅による打ち切り誤差と丸め誤差、変化の速い関数の微分を扱います。

## 内容・演習

10進数0.1の2進表現と、0.01を繰り返し加える例から有限精度を確認します。数値微分では、差分公式の次数だけでなく、差分を刻み幅で割ることで丸め誤差が増える点を説明します。`sin(x)`と`sin(10^4 x)`を数値微分し、誤差が小さくなる刻み幅を比べます。

2の補数の説明は、符号と絶対値を別々に格納する方式との混同を避けるため訂正しています。64 bit浮動小数点数は、符号1 bit・指数部11 bit・仮数部52 bitを持ち、正規化数では暗黙の先頭bitを含めて53 bitの有効精度です。大きさが異なる数の加算による情報落ちと、近い数の減算による桁落ちも分けて説明しています。

Notebookには次の演習用セルを空欄で残しています。

1. 多項式の数値微分を解析解と比較する。
2. 振動数の高い正弦関数で、刻み幅による誤差の違いを調べる。
3. 3種類の差分公式を比較し、小さすぎる刻み幅の影響を確認する。

## PDFと図の再生成

`2026/week6`で実行します。図を作り直してから、Beamerを組版します。

```sh
MPLCONFIGDIR=/tmp/weeks6-8/mpl python3 make_figures.py
TEXMFVAR=/tmp/weeks6-8/texmf-var TEXMFCACHE=/tmp/weeks6-8/texmf-var \
  latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=.beamer-build slide.tex
cp .beamer-build/slide.pdf slide.pdf
```

図はNumPyとMatplotlibで生成します。LuaLaTeX、Beamer、LuaTeX-jaと共通テーマのフォントが必要です。

## 確認内容

PDFは21ページです。全ページをPNG化して版面を確認し、最終組版ログにoverfull/underfull、欠落文字、LaTeXエラーがないことを確認しました。Notebookは13セルで、4個の実行可能コードセルを新しいPython環境で実行しました。数値微分のassertを通過し、3つの演習セルは空欄のままです。

Colabで開いた場合は「ファイル」メニューからドライブにコピーを保存してください。
