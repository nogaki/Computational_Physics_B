# 第十四回：根の探索

[2025年度のスライド](../../2025/week14/week14.pdf)と[実習ノートブック](../../2025/week14/week14.ipynb)を元に、[共通Beamerテーマ](../../templates/beamer/README.md)で作成しています。講義日は2027年2月2日、著者は野垣 康介、藤本 悠輝です。

- [slide.tex](slide.tex)：編集用のLaTeX。
- [slide.pdf](slide.pdf)：17ページの配布資料。
- [week14.ipynb](week14.ipynb)：二分法、Newton法、割線法、固定点反復のNotebook。
- [make_figures.py](make_figures.py)：方法ごとの数値反復から図を生成。
- `figures/`：二分法の区間とNewton法の接線、3手法の残差比較。

本文と数式は編集可能なLaTeX、計算例は編集可能なPythonです。4:3形式で本文は12ptです。

## 内容

二分法では、連続関数の符号変化から根を含む区間を縮めます。単調性は必要条件ではありません。Newton法はTaylor展開と接線から導き、導関数が0になる場合や初期値に依存する点を確認します。割線法は導関数を差分で近似し、固定点反復では写し方と局所収束条件を扱います。

講義資料の演習関数は次の3つです。

- `f(x)=x^3-x-2`
- `g(x)=cos(x)-x`
- `h(x)=log(x)+x-3`

演習では3関数すべてを二分法で解き、`h`は対数の定義域`x>0`で区間を選びます。さらに3関数をNewton法・割線法で解き、`g,h`を固定点形式に書き直します。

演習の解答はNotebookに追加せず、最後のコードセルを空欄にしています。

## 図の条件

- `root_geometry.pdf`：`f(x)=x^3-x-2`、二分法の初期区間`[1,2]`、Newton法の初期値`x0=1.3`。関数を実線、接線を破線、Newton更新点と近似根を点で示します。
- `root_convergence.pdf`：同じ関数で二分法`[1,2]`、Newton法`x0=1.5`、割線法`x0=1, x1=2`を実行し、各反復の残差`|f(x_n)|`を対数軸で表示します。二分法は赤実線・丸、Newton法は青破線・四角、割線法は緑点線・三角です。

## 図の再生成とPDFのビルド

`2026/week14`で実行します。

```sh
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/weeks12-14/mpl python3 make_figures.py
TEXMFVAR=/tmp/weeks12-14/texmf-var TEXMFCACHE=/tmp/weeks12-14/texmf-var \
  latexmk -lualatex -interaction=nonstopmode -halt-on-error \
  -outdir=.beamer-build slide.tex
cp .beamer-build/slide.pdf slide.pdf
```

図の生成にはPython、NumPy、Matplotlibを使います。PDFの組版にはLuaLaTeX、Beamer、LuaTeX-ja、テンプレート指定のフォントが必要です。

## Notebook

GitHubで`week14.ipynb`を開き、Colabの「ファイル」→「ノートブックを開く」→「GitHub」から読み込めます。開いた後は「ドライブにコピーを保存」を実行してください。Notebookの例はPython標準ライブラリだけで実行できます。

Notebookは19セルで、12個のコードセルを新しいカーネルで実行済みです。二分法、Newton法、割線法、固定点反復の例は残差を確認し、`assert`で根を検査します。導関数が0になるNewton法と、割線法の分母が0になる場合も安全に停止することを確認しています。演習セルは空欄です。

## 数値上の条件と修正

- 二分法は端点で関数値が0ならその点を返し、それ以外は有限な区間と符号変化を要求します。連続性は数学上の前提で、コードから自動判定はできません。
- Newton法は関数値、導関数、ステップの有限性を確認し、残差とステップ幅、最大反復回数で終了を管理します。
- 割線法は2つの初期値を使い、分母が0になる場合と最大反復回数を確認します。
- 元スライドの「単調増加（減少）」は二分法の必要条件ではないため、連続性と符号変化に修正しました。
- 原Notebookの多項式例、導関数、固定点の緩和例を引き継ぎ、講義スライドにある`f,g,h`は問題文と空欄だけを追加しました。
- LuaLaTeXで17ページを作成し、全ページをPNGとコンタクトシートで確認しました。組版のはみ出しと欠落文字はありません。

## 参考

- 野本拓也・是常隆・有田亮太郎『実践計算物理学』共立出版。
- [SciPy: `bisect`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.bisect.html)
