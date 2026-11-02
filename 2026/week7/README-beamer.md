# 第7回スライド（Beamer版）

[2025年度の第7回PDF](../../2025/week7/week7.pdf)と[実習ノートブック](../../2025/week7/week7.ipynb)を元に、[共通テンプレート](../../templates/beamer/README.md)で作成しています。講義日は2026年12月1日、著者は野垣 康介、藤本 悠輝の順です。

- [編集用スライド](slide.tex)
- [配布用PDF](slide.pdf)
- [実習ノートブック](week7.ipynb)
- [図の再生成スクリプト](make_figures.py)
- `figures/`: 中点則・台形則・シンプソン則、収束、Runge現象の図

表紙1枚と本文39枚の計40ページです。2025年度版の40ページに含まれていた公式と例を保ち、内容が重なる図や説明をまとめています。

## 内容・例・演習

中点則・台形則・シンプソン則の1区間公式と合成公式、誤差の次数、Richardsonによる適応求積、Romberg積分を扱います。不連続点では積分区間を分け、端点特異点は$x=t^2$で変換します。半無限区間と両側無限区間の変数変換も導出します。

Lagrange補間からNewton--Cotes公式を導き、等間隔の高次補間で起こるRunge現象を示します。Gauss--Legendre公式の積分点・重みと区間変換を追加し、NumPyの`leggauss`を使うNotebook例で4点公式が$x^7$を厳密に積分することを確認します。

Notebookは2025年度の実習順を保ち、3つの求積則の図とアニメーション、適応求積、不連続関数、端点特異点、無限区間の例を残しています。アニメーションは既存のPillowを使い、追加ライブラリを必要としない形にしています。誤差式は合成則の端点導関数による形に直し、半無限区間変換の微分を

$$
dx=\frac{dt}{(1-t)^2}
$$

に訂正しています。端点特異点の台形則は非有限値を表示し、Notebook全体の実行を止めません。分割数は正であること、シンプソン則では偶数であることを確認します。

最終演習は、$\int_0^2x^7\,dx=32$を中点則・シンプソン則で$N=4,16,64$として比較します。解答用コードセルは空欄です。2025年度版の中間レポート締切は引き継がず、「課題・レポートの提出方法・期限は授業で案内します」としています。

## PDFと図の再生成

`2026/week7`で実行します。

```sh
MPLCONFIGDIR=/tmp/weeks6-8/mpl python3 make_figures.py
TEXMFVAR=/tmp/weeks6-8/texmf-var TEXMFCACHE=/tmp/weeks6-8/texmf-var \
  latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=.beamer-build slide.tex
cp .beamer-build/slide.pdf slide.pdf
```

図はNumPyとMatplotlibで生成します。Notebook実行にはNumPy、Matplotlib、Pillowが必要です。LuaLaTeX、Beamer、LuaTeX-jaと共通テーマのフォントが必要です。

## 確認内容

PDFは40ページです。全ページをPNG化して版面を確認し、最終組版ログにoverfull/underfull、欠落文字、LaTeXエラーがないことを確認しました。Notebookは67セルで、46個のコードセルを新しいPython環境で実行し、エラーがないことを確認しました。4点Gauss--Legendre積分のassertを通過し、演習セル1つは空欄です。

## 参考資料

- 水島二郎・柳瀬眞一郎『理工学のための数値計算法』数理工学社
- 野本拓也・是常隆・有田亮太郎『実践計算物理学』共立出版
- [PHYS6350 Computational Physics](https://github.com/vlvovch/PHYS6350-ComputationalPhysics)

Colabで開いた場合は「ファイル」メニューからドライブにコピーを保存してください。
