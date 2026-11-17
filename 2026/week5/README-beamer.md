# 第5回スライド（Beamer版）

[2025年度の第5回PDF](../../2025/week5/week5.pdf)と[実習ノートブック](../../2025/week5/week5.ipynb)を元に、[共通テンプレート](../../templates/beamer/README.md)で作成しています。講義日は2026年11月17日、著者は野垣 康介、藤本 悠輝の順です。

- [slide.tex](slide.tex)：編集用のLaTeXソース。
- [slide.pdf](slide.pdf)：配布用PDF。
- [week5.ipynb](week5.ipynb)：実習ノートブック。
- [pulsar.csv](pulsar.csv)：付録Aで使うATNFパルサーカタログのデータ。
- [make_figures.py](make_figures.py)：スライド内のグラフの再生成用コード。
- `figures/`：グラフと粒子識別の引用図。

第1〜4回と同じ4:3のBeamer形式で、全36ページです。本編の実習5問は22〜23ページの「実習タイム」にまとめています。24ページからは付録と発展課題です。グラフはMatplotlibで再生成し、粒子識別の比較図は元資料から出典表示を含めて抽出しています。

## 内容

本編では、点と折れ線、凡例、軸ラベル、PDF保存を学びます。実習1では第4回で扱ったガウス型関数を21点と6点で重ね描きし、ピークの見え方を比べます。実習2ではばねに加えた力と伸びの散布図に比例関係を表す直線を重ね、直線からのずれを調べます。

小さな格子で `meshgrid` の出力を確認したあと、同じ二変数のガウス型関数を等高線・塗りつぶし等高線・密度プロットで描きます。実習3では関数の式を変え、中心を移した等高線を学生が描き直します。

実習4では3本の比例直線の残差を比較して5点に最もよく合う直線を選び、実習5では塗りつぶし等高線と密度プロットを使ってガウス型関数の幅の変化を調べます。

付録Aではパルサーの両対数散布図と粒子識別の例を紹介し、付録Bでは双極子を使って塗りつぶし等高線、密度表示、3次元表示を扱います。Bessel関数とフラクタルは発展課題です。

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

ColabではNotebookを開いてドライブにコピーを保存します。本編ではNumPyとMatplotlibを使います。

パルサーの付録を実行する場合は、`pulsar.csv`をダウンロードしてColabの「ファイル」へアップロードします。ローカルではNotebookとCSVを同じディレクトリに置きます。サイクロイドのアニメーションはNotebookの発展例です。

## 図の前提

- `cos(x)`の点は0〜10 radで11個または101個です。元資料の「10個」は11個に訂正しています。
- ばねの散布図は5組の仮想測定値を使います。
- パルサーの図は付属CSVの固定データを使います。取得時点は元資料に記録されていません。対数軸では`P0`・`P1`が有限かつ正の行のみを表示し、欠損値・非正値を除きます。等磁場・等特性年齢の線は単純化した磁気双極子模型による推定の目安です。
- 双極子の図は無次元量です。正電荷を(-2, 0)、負電荷を(2, 0)に置き、特異点を避けるため各電荷から距離0.25未満を表示から除きます。密度表示の色範囲は-1.5〜1.5、3次元図の表示範囲は-5〜5です。表示範囲外でポテンシャルが一定になる意味ではありません。
- マンデルブロ集合の図は、有限回の反復による近似です。

## 確認内容

LuaLaTeXで36ページを生成し、版面を確認しました。組版のはみ出しや欠落文字の警告はありません。

Notebookは50セルです。IPython環境で本編と双極子・アニメーションのコード例を実行し、本編5問は作図まで確認しました。授業内と発展課題の計7つの解答セルは空欄です。パルサーは保存済みの出力を掲載し、CSVの表示対象2,746件を別途照合しました。付録Aのpandasでの再実行とColab上での動作は今回未確認です。

## 参照

- 『実践計算物理学』野本拓也・是常隆・有田亮太郎（共立出版）
- [PHYS6350 Computational Physics](https://github.com/vlvovch/PHYS6350-ComputationalPhysics)
- [Matplotlib公式ドキュメント](https://matplotlib.org/stable/)
- [Matplotlib：図の保存](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html)
- [Matplotlib：3次元曲面](https://matplotlib.org/stable/gallery/mplot3d/surface3d.html)
- [ATNFパルサーカタログ](https://www.atnf.csiro.au/research/pulsar/psrcat/)
- [ALICE Collaboration：First results of the ALICE detector performance at 13 TeV](https://cds.cern.ch/record/2047855)
- [SciPy：第一種Bessel関数](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.jv.html)
