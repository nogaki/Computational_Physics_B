# 第9回：モンテカルロ法 II

2次元正方格子Ising模型を題材に、Metropolis更新、スピン反転のエネルギー差、磁化、自己相関、熱平衡化、有限サイズの温度依存性を扱います。Notebookは磁化とエネルギーの標本を作り、磁化二乗平均と比熱を求める演習を含みます。

## コンパイル

`2026/week9`で実行します。

```sh
latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=.beamer-build slide.tex
```

PDFは`.beamer-build/slide.pdf`に生成されます。配布用PDFを更新するには`cp .beamer-build/slide.pdf slide.pdf`を実行します。LuaLaTeX、Beamer、LuaTeX-jaと共通テーマのフォントが必要です。

図を再生成するときはNumPyとMatplotlibを使います。

```sh
python3 make_figures.py
```

固定seedの有限格子Isingシミュレーションから、配位、磁化系列、温度依存性を描きます。温度依存性の図は説明用の短い計算で、臨界指数や転移点を精密推定するものではありません。

## Notebook

GitHubで`2026/week9/week9.ipynb`を開き、Colabの「ファイル」→「ノートブックを開く」→「GitHub」から開きます。開いた後は「ドライブにコピーを保存」を選び、セルを先頭から順に実行してください。ローカルではNotebookと同じPython環境にNumPy、Matplotlibが必要です。

Notebookは20×20格子を使います。磁化系列は12万回、温度走査は各温度18万回のスピン反転試行です。温度走査は数秒から十数秒かかる場合があります。試行回数を減らせば短時間で動きますが、統計誤差が増えます。

## 原資料からの訂正・補足

- $J>0$ の最近接強磁性、外場$h=0$、周期境界条件を明記しました。Notebookでは$J=k_{\rm B}=1$とし、温度を$k_{\rm B}T/J$で表します。
- 周期境界を含む反転エネルギー差を$\Delta E=2Js_i\sum_{j\in\mathrm{nn}(i)}s_j$とし、全エネルギー差との一致をassertで確かめます。
- 有限系で符号反転を含む磁化平均$\langle m\rangle$と秩序の大きさ$\langle|m|\rangle$を区別しました。無限格子の自発磁化式との比較は有限サイズ効果を含むことも示しています。
- 受理率から独立な配位間隔を決める原資料の説明を改めました。バーンインは初期条件の影響を減らす区間の除外、測定の間引きは自己相関への対処であり、間引きだけで独立性は保証されません。$L^2/\text{受理率}$は粗いサイト更新の目安としてのみ説明します。
- 2次元正方格子の臨界温度は$k_{\rm B}T_c/J=2/\ln(1+\sqrt2)$としました。有限サイズの臨界点近くにおける非ゼロの$\langle|m|\rangle$を無限系の厳密解と同一視しません。
- 原PDFの最終演習（$\langle m^2\rangle$と比熱）をNotebookに空欄付きで残しました。

## 参照

- 2025年度資料：`../../2025/week9/week9.pdf`、`../../2025/week9/week9.ipynb`
- 『実践計算物理学』野本拓也・是常隆・有田亮太郎（共立出版）
