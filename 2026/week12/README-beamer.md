# 第十二回：偏微分方程式1

[2025年度のスライド](../../2025/week12/week12.pdf)と[実習ノートブック](../../2025/week12/week12.ipynb)を元に、[共通Beamerテーマ](../../templates/beamer/README.md)で作成しています。講義日は2027年1月19日、著者は野垣 康介、藤本 悠輝です。

- [slide.tex](slide.tex)：編集用のLaTeX。
- [slide.pdf](slide.pdf)：24ページの配布資料。
- [week12.ipynb](week12.ipynb)：実習用ノートブック。
- [make_figures.py](make_figures.py)：差分法を実計算して図を再生成するコード。
- `figures/`：ラプラス方程式の電位、熱伝導の数値解、FTCS法の増幅率。
- [heat_equation_1D_implicit.gif](heat_equation_1D_implicit.gif)：陰解法による温度分布のアニメーション。

本文・数式・コードは編集可能です。4:3形式で、本文とコード抜粋は12ptです。

## 内容

偏微分方程式の境界値問題と初期値問題を扱います。2次元ラプラス方程式を5点差分で離散化し、Jacobi法、Gauss--Seidel法、SOR法の更新を導きます。NotebookではJacobi法とSOR法を実行して残差を確認します。熱方程式ではFTCS法の更新式とvon Neumann安定性解析を導き、陰解法とCrank--Nicolson法を紹介します。実習では1次元波動方程式をCrank--Nicolson法で解きます。ラプラス問題の格子では、上辺の角を除いた点を電位\(V\)、ほかの境界点を0とします。

## 図の再生成とPDFのビルド

`2026/week12`で実行します。

```sh
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/weeks12-14/mpl python3 make_figures.py
TEXMFVAR=/tmp/weeks12-14/texmf-var TEXMFCACHE=/tmp/weeks12-14/texmf-var \
  latexmk -lualatex -interaction=nonstopmode -halt-on-error \
  -outdir=.beamer-build slide.tex
cp .beamer-build/slide.pdf slide.pdf
```

Python図の生成にはNumPy、Matplotlib、SciPyを使います。PDFの組版にはLuaLaTeX、Beamer、LuaTeX-ja、テンプレートで指定するフォントが必要です。

## Notebook

GitHubで`week12.ipynb`を開き、Colabの「ファイル」→「ノートブックを開く」→「GitHub」から読み込めます。開いた後は「ドライブにコピーを保存」を実行してください。ローカルではNotebookと同じフォルダで実行します。NumPy、Matplotlib、SciPyを使います。

Notebookは32セルで、15個の実行可能なコードセルを実行済みです。Jacobi法とSOR法の離散残差を確認し、熱方程式の安定・不安定な刻み幅を実行しました。意図的に不安定なFTCS例は、`r=0.6`で8ステップに限り、有限値のまま増幅を観察します。波動方程式の実習セルは空欄です。

## 変更点と数値条件

- 「PythonにPDEライブラリがない」という記述は削除し、「今回は差分式を自分で実装する」としました。配列計算にはNumPy、三重対角方程式にはSciPyを使います。
- SORの緩和係数は標準的な定義に統一しました。2次元ラプラス問題では`0 < omega < 2`が収束範囲です。
- 熱方程式のFTCS安定条件は`r = D dt / dx^2 <= 1/2`です。資料中の安定解析とNotebookの刻み幅を一致させました。
- 波動方程式のCrank--Nicolson連立方程式を、時間平均の式から導き直しました。最後の実習コードセルには解答を記入していません。
- 温度分布の図は、長さ1 cm、熱拡散率`4.25e-6 m^2/s`の棒を格子40点で計算した表示例です。Notebookでは格子100点の例も実行します。

## 確認

LuaLaTeXで24ページを作成し、全ページをPNGにしてコンタクトシートで確認しました。組版のはみ出しと欠落文字はありません。Notebookは新しいインプロセスカーネルでコードセルを順番に実行し、全15セルがエラーなく完了しました。アニメーションを含む出力を保存しています。

## 参考

- 野本拓也・是常隆・有田亮太郎『実践計算物理学』共立出版。
- M. Newman, *Computational Physics*.
- [PHYS6350 Computational Physics](https://github.com/vlvovch/PHYS6350-ComputationalPhysics)
