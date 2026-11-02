# 第十回：常微分方程式1

初期値問題を題材にEuler法、RK2法、RK4法、連立方程式、2階運動方程式、硬い方程式、陽解法・陰解法、適応刻み幅制御を扱います。単振り子の実習用セルは未完成のまま残し、最後にSciPyの`solve_ivp`を紹介します。

## コンパイル

`2026/week10`で実行します。

```sh
latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=.beamer-build slide.tex
cp .beamer-build/slide.pdf slide.pdf
```

LuaLaTeX、Beamer、LuaTeX-jaと共通テーマのフォントが必要です。図を作り直す場合はNumPyとMatplotlibを使います。

```sh
python3 make_figures.py
```

## Notebook

GitHubで`2026/week10/week10.ipynb`を開き、Colabの「ファイル」→「ノートブックを開く」→「GitHub」から開きます。開いたら「ドライブにコピーを保存」を選び、先頭からセルを実行してください。ローカル実行ではNumPy、Matplotlib、SciPyが必要です。

Notebookは31セルで、17個の実行セルと単振り子の解答用セル1個を含みます。固定データや乱数は使わないためseed設定はありません。主要な演算は短時間で終わります。

## 原資料からの訂正・補足

- 単振り子の左辺をトルクの式$mL^2\ddot\theta=-mgL\sin\theta$に訂正しました。したがって角加速度は$-(g/L)\sin\theta$です。
- RK4の適応刻み幅をstep-doublingで実装しました。2025年度版は許容誤差を単位時間あたりの$\delta$とし、1ステップの目標を$h\delta$に置くため、差分式の$h$因子と4乗根はその定義に対応します。2026年度版では1ステップの絶対許容誤差$\mathrm{atol}$を使い、長さ$h$の1ステップと$h/2$の2ステップの差から誤差を$|x_{h/2}^{(2)}-x_h|/15$と見積もります。誤差次数5に合わせて5乗根で刻み幅を更新します。
- 陰Euler法は硬い線形問題で安定でも、大きな刻み幅では精度が低いことを示しました。
- 時間刻みの細分化による誤差次数を解析解$x(t)=e^{-t}$と比較してassertで確認します。適応RK4の解とSciPyの`solve_ivp`も成功条件・解析解で確認します。
- SciPyの右辺関数を正しい`fun(t, y)`順にし、`success`と終端時刻を確認します。

## 参照

- 2025年度資料：`../../2025/week10/week10.pdf`、`../../2025/week10/week10.ipynb`
- 『実践計算物理学』野本拓也・是常隆・有田亮太郎（共立出版）
- 『理工学のための数値計算法』水島二郎・柳瀬眞一郎（数理工学社）
