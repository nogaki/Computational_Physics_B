# 第5回スライド（Beamer版）

[2025年度の第5回PDF](../../2025/week5/week5.pdf)と[実習ノートブック](../../2025/week5/week5.ipynb)を元に、[共通テンプレート](../../templates/beamer/README.md)で作成しています。講義日は2026年11月17日、著者は野垣 康介、藤本 悠輝の順です。

- [slide.tex](slide.tex)：編集用のLaTeXソース。
- [slide.pdf](slide.pdf)：配布用PDF。
- [week5.ipynb](week5.ipynb)：実習ノートブック。
- [pulsar.csv](pulsar.csv)：元教材に付属するATNFパルサーカタログのデータ。
- [make_figures.py](make_figures.py)：スライド内のグラフの再生成用コード。
- `figures/`：グラフと粒子識別の引用図。

第1〜4回と同じ4:3のBeamer形式で、表紙1枚と本文27枚の計28ページです。本文・数式・コードをLaTeXで編集できます。本文とコードは12ptです。グラフはMatplotlibで再生成し、粒子識別の比較図は元資料から出典表示を含めて抽出しています。

## 内容

配列の要素を取り出す`for`文を復習し、Matplotlibの読み込み、点と折れ線、凡例と線種、PDF保存を扱います。点数不足・軸ラベル不足・区別しにくい線種の例を通して、図を読むために必要な情報を確認します。

散布図の例は模擬測定、加速器実験の粒子識別、パルサーの周期と周期変化率です。2変数の例には電気双極子のポテンシャルを使い、`meshgrid`、等高線、塗りつぶした等高線、密度表示、3次元表示を扱います。第一種Bessel関数の作図・PDF提出と、フラクタルの発展課題を含みます。

## コンパイルと図の再生成

`2026/week5`で実行します。

```sh
latexmk -lualatex -interaction=nonstopmode -halt-on-error slide.tex
```

LuaLaTeX、Beamer、LuaTeX-jaと共通テーマのフォントが必要です。フォントとデザインの詳細は[テンプレートの説明](../../templates/beamer/README.md)を参照してください。

図を変更する場合は、先に以下を実行します。NumPy、Matplotlib、pandas、SciPyを使います。生成済みの図を利用してPDFを組版するだけなら、Pythonの実行は不要です。

```sh
python3 make_figures.py
latexmk -lualatex -interaction=nonstopmode -halt-on-error slide.tex
```

`figures/particle_identification.pdf`は2025年度PDFの17ページから、左右の図と出典を切り出したものです。再計算する図ではないため、このスクリプトでは上書きしません。

## Notebookとデータ

ColabではNotebookを開いてドライブにコピーを保存し、同じフォルダの`pulsar.csv`をダウンロードしてColabの「ファイル」へアップロードします。ローカルではNotebookとCSVを同じディレクトリに置いて実行してください。

元の実習例を引き継ぎ、軸ラベル、対数軸に渡すデータの選別、3次元座標の作り方を修正しています。Bessel関数と発展課題の解答セルは空欄です。サイクロイドのアニメーションはNotebookの発展例として残しています。

## 図の前提

- `cos(x)`の点は0〜10 radで11個または101個です。元資料の「10個」は11個に訂正しています。
- 模擬測定の散布図は実測データではありません。
- パルサーの図は付属CSVの固定データを使います。取得時点は元資料に記録されていません。対数軸では`P0`・`P1`が有限かつ正の行のみを表示し、欠損値・非正値を除きます。等磁場・等特性年齢の線は単純化した磁気双極子模型による推定の目安です。
- 双極子の図は無次元量です。正電荷を(-2, 0)、負電荷を(2, 0)に置き、特異点を避けるため各電荷から距離0.25未満を表示から除きます。密度表示の色範囲は-1.5〜1.5、3次元図の表示範囲は-5〜5です。表示範囲外でポテンシャルが一定になる意味ではありません。
- マンデルブロ集合の図は、有限回の反復による近似です。

## 確認内容

LuaLaTeXで28ページを生成し、全ページを画像化して版面を確認しました。組版のはみ出しや欠落文字の警告はありません。スライドの17個のコード抜粋は、明記した前提のデータを準備して実行しました。

Notebookは33セルです。IPython環境で16個のコード例を順に実行し、グラフとアニメーションを含む出力を保存しています。2つの解答セルは空欄です。パルサーの表示対象2,746件、双極子の200×200の配列と符号の対称性、元CSVとの一致を確認しています。Colab上での実行は未確認です。

## 参照

- 『実践計算物理学』野本拓也・是常隆・有田亮太郎（共立出版）
- [PHYS6350 Computational Physics](https://github.com/vlvovch/PHYS6350-ComputationalPhysics)
- [Matplotlib公式ドキュメント](https://matplotlib.org/stable/)
- [Matplotlib：図の保存](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html)
- [Matplotlib：3次元曲面](https://matplotlib.org/stable/gallery/mplot3d/surface3d.html)
- [ATNFパルサーカタログ](https://www.atnf.csiro.au/research/pulsar/psrcat/)
- [ALICE Collaboration：First results of the ALICE detector performance at 13 TeV](https://cds.cern.ch/record/2047855)
- [SciPy：第一種Bessel関数](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.jv.html)
