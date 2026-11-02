# 第十三回：偏微分方程式2

[2025年度のスライド](../../2025/week13/week13.pdf)、[波動方程式Notebook](../../2025/week13/Wave.ipynb)、[Schrödinger方程式Notebook](../../2025/week13/Schrodinger.ipynb)を元に、[共通Beamerテーマ](../../templates/beamer/README.md)で作成しています。講義日は2027年1月26日、著者は野垣 康介、藤本 悠輝です。

- [slide.tex](slide.tex)：編集用のLaTeX。
- [slide.pdf](slide.pdf)：22ページの配布資料。
- [week13.ipynb](week13.ipynb)：2冊のNotebookへの案内と実行順。
- [Wave.ipynb](Wave.ipynb)：波動方程式の実習を完成させ、3方式を比較。
- [Schrodinger.ipynb](Schrodinger.ipynb)：原子単位系でガウス波束の障壁散乱を計算。
- [make_figures.py](make_figures.py)：スライド用の図を数値計算から再生成。
- `figures/`：波動方程式の離散エネルギーと波束散乱の図。
- [wave_equation_1D_CrankNicolson.gif](wave_equation_1D_CrankNicolson.gif)、[gauss_barrier_scattering.gif](gauss_barrier_scattering.gif)：各Notebookから保存した計算アニメーション。

4:3形式で、本文とコード抜粋は12ptです。内容は編集可能なLaTeXとNotebookで提供しています。

## 内容

固定端の波動方程式を1階連立系に書き直し、FTCS法、陰解法、Crank--Nicolson法の安定性とエネルギーを比較します。FTCS法の不安定性は、Notebookで用いる前進Euler更新に限った結論として示します。

後半では時間依存Schrödinger方程式を原子単位系で解きます。時間に依存しない実ポテンシャルの離散Hamiltonianを内部格子点に作り、端点の波動関数を0に固定してCrank--Nicolson法で時間発展させます。ガウス波束が幅0.5 Bohr、高さ36.2 Hartreeの障壁に散乱される例を扱います。実習ではポテンシャルの高さ・幅・形状を変えて散乱を調べます。

## 図の条件

- `wave_energy.pdf`：`L=1`、`N=100`、`v=0.1`、`dt=0.01`、初期変位`sin(40 pi x/L)`、初期速度0。0から1まで100ステップ計算し、離散エネルギー比を実線（FTCS）・破線（陰解法）・一点鎖線（Crank--Nicolson）で表示します。
- `wave_packet_scattering.pdf`：`x0=-10 Bohr`、`sigma=1.8 Bohr`、`k0=10 Bohr^-1`、障壁幅0.5 Bohr・高さ36.2 Hartree。`[-40,40] Bohr`を3200区間（`dx=0.025 Bohr`）、`dt=0.004`原子時間単位で計算し、`t=0, 1.6, 2.4, 2.8`における確率密度を描きます。灰色の障壁は高さを160で割って表示します。終了時刻では波束は障壁内にほぼ残らず、領域端にも到達していません。

## 図の再生成とPDFのビルド

`2026/week13`で実行します。

```sh
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/weeks12-14/mpl python3 make_figures.py
TEXMFVAR=/tmp/weeks12-14/texmf-var TEXMFCACHE=/tmp/weeks12-14/texmf-var \
  latexmk -lualatex -interaction=nonstopmode -halt-on-error \
  -outdir=.beamer-build slide.tex
cp .beamer-build/slide.pdf slide.pdf
```

Python図の生成にはNumPy、Matplotlib、SciPyを使います。LuaLaTeXの組版にはBeamer、LuaTeX-ja、テンプレート指定のフォントが必要です。

## Notebookの実行

案内Notebookの[week13.ipynb](week13.ipynb)からColabリンクを開き、まず`Wave.ipynb`、次に`Schrodinger.ipynb`を実行します。それぞれ「ファイル」→「ドライブにコピーを保存」を選んで自分用のコピーを作ってください。ローカルでは同じフォルダのNotebookを個別に実行します。NumPy、Matplotlib、SciPy、MatplotlibのGIF保存用Pillowが必要です。

`Wave.ipynb`は19セルで、10個のコードセルを新しいカーネルで実行済みです。FTCSの意図的な不安定例は100ステップに制限し、数値が有限な間に増幅を確認します。陰解法では`E(1)/E(0)=0.25347`、Crank--Nicolson法では1に保たれました。波動方程式の1周期を示すGIFも保存しています。

`Schrodinger.ipynb`は6セルで、3個のコードセルを実行済み、末尾の実習セルは空欄です。障壁は原点中心で`|x| <= width/2`とし、離散Hamiltonianは内部点だけに作成します。端点は全時刻で`psi=0`です。`dt=0.004`、最終時刻2.8原子時間単位ではノルムの最大ずれが`1.70e-13`、反射確率が`0.133070`、透過確率が`0.866930`、障壁内の確率が`3.23e-15`でした。

ノルム保存は時間発展の離散的な性質であり、空間精度を保証しません。空間区間を3200から6400へ倍にすると反射確率は`0.133070`から`0.139242`、透過確率は`0.866930`から`0.860758`へ変わりました。スライドとNotebookの数値は指定した格子での結果で、連続系の収束値として扱いません。

## 修正と確認

- 波動方程式のCrank--Nicolson三重対角方程式を、2本の更新式から導き直してNotebookとスライドを一致させました。
- 2025年度NotebookのSchrödinger障壁は指定幅より広くなっていたため、中心を0とする幅`barrier_width`の矩形障壁に修正しました。
- 有限領域の端点を固定する境界条件を、説明・差分行列・コードで一致させました。散乱計算は波束が端で反射する前の時刻で止めています。
- 2025年度資料中の`np.trapz`を`np.trapezoid`に修正しました。
- LuaLaTeXで22ページを作成し、全ページをPNGとコンタクトシートで確認しました。組版のはみ出しと欠落文字はありません。二つの計算Notebookは新しいインプロセスカーネルで上から実行し、すべての実行セルがエラーなく完了しました。

## 参考

- 野本拓也・是常隆・有田亮太郎『実践計算物理学』共立出版。
- [Numerical solution of the time-dependent Schrödinger equation](http://staff.ustc.edu.cn/~zqj/posts/Numerical_TDSE/)
- [PHYS6350 Computational Physics](https://github.com/vlvovch/PHYS6350-ComputationalPhysics)
