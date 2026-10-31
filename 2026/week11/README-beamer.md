# 第十一回：常微分方程式2

SciPyの初期値問題ソルバー、Lorenz方程式、二重振り子、分子動力学を扱います。Notebookは原資料と同じ名前の`Lorenz.ipynb`、`DoublePendulum.ipynb`、`MolecularDynamics.ipynb`で分け、`week11.ipynb`を入口にしました。

## コンパイル

`2026/week11`で実行します。

```sh
latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=.beamer-build slide.tex
cp .beamer-build/slide.pdf slide.pdf
```

LuaLaTeX、Beamer、LuaTeX-jaと共通テーマのフォントが必要です。

## Notebookと図

GitHubで`2026/week11/week11.ipynb`を開き、Colabの「ファイル」→「ノートブックを開く」→「GitHub」から開きます。「ドライブにコピーを保存」を選び、開きたい個別Notebookを上から順に実行します。ローカル実行にはNumPy、Matplotlib、SciPyが必要です。

図を作り直す場合は、3つの個別Notebookを実行して出力を保存した後、NumPy、Matplotlib、nbformatがある環境で次を実行します。

```sh
python3 make_figures.py
```

スクリプトは実行済みNotebookに埋め込まれたLorenz、二重振り子、MDの図を`figures/`へ抽出し、LJポテンシャルとleapfrogの時刻配置図を再生成します。`phase_diagram.png`は2025年度PDF 17ページの文献図だけを切り出したものです。

Lorenz例は区間$0\le t\le40$を4001出力点で計算します。二重振り子は10秒を積分し、121フレームのアニメーションを作ります。MD例は64粒子、1000ステップ、1試行あたり全粒子対を調べるため、他のNotebookより実行に時間がかかります。MDの計算量は概ね$N^2$とステップ数の積に比例します。

実行確認ではLorenzの4セル、二重振り子の4セル、MDの9セルを新しいIPythonカーネルで実行しました。二重振り子のHTMLアニメーションも生成しています。

## 原資料からの訂正・前提

- SciPyの右辺関数を`fun(t, y)`順とし、`solve_ivp`の`success`と出力配列を確認します。Lorenz軌道は有限時間の近似で、カオス系の長期予測として扱いません。
- 二重振り子の角加速度は質量行列を`numpy.linalg.solve`で解きます。角度差の正弦・余弦を分母とする個別除算は避けました。この初期条件では全エネルギーの初期値がほぼ0なので、エネルギー確認は相対変動ではなく最大絶対変動で行い、$1.09\times10^{-7}\,\mathrm{J}$でした。
- Lennard--Jones模型の無次元温度を$k_{\rm B}T/\epsilon$とします。原資料の相図はS. Stephan, M. Thol, J. Vrabec, H. Hasse, *Journal of Chemical Information and Modeling* **59**, 4248 (2019) の文献図です。Notebookの短時間MD条件から相境界を推定した図ではありません。
- MDでは最小像規約に合わせて$r_c=L/2$で相互作用を打ち切り、ポテンシャルと力がカットオフで0となるforce-shiftを使います。全ての周期像を足し上げる長距離LJ計算とは異なり、エネルギー・圧力の尾部補正も加えていません。
- 初期速度標本から実測$T_{\rm kin}$を計算し、初期圧力にも同じ$P=\rho k_{\rm B}T_{\rm kin}+P_{\rm virial}$を使います。重心速度は除いていないため、温度は$3N$自由度で定義します。
- $Z=P/(\rho k_{\rm B}T_{\rm kin})$は圧縮因子であり、等温圧縮率$\kappa_T$ではありません。
- 速度Verlet法は全エネルギーを厳密保存しません。この実行では最大エネルギー変動が粒子あたり$4.805\times10^{-3}$でした。初期分布パラメータ$T_0=1$と、有限標本から測った初期温度$1.070$も区別します。

## 参照

- 2025年度資料：`../../2025/week11/week11.pdf`、`../../2025/week11/Lorenz.ipynb`、`../../2025/week11/DoublePendulum.ipynb`、`../../2025/week11/MolecularDynamics.ipynb`
- Lennard--Jones相図：S. Stephan et al., *J. Chem. Inf. Model.* 59, 4248 (2019)。図の出典は原資料17ページに記載。
- SciPy公式ドキュメント：[`scipy.integrate.solve_ivp`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html)
