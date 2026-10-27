# 第4回スライド（Beamer版）

[2025年度の第4回PDF](../../2025/week4/week4.pdf)と[実習ノートブック](../../2025/week4/week4.ipynb)を元に、[共通テンプレート](../../templates/beamer/README.md)で作成しています。本編は表紙1枚と本文16枚の17ページ、付録も表紙1枚と本文16枚の17ページで、配布PDFは合計34ページです。講義日は2026年11月10日、著者は野垣 康介、藤本 悠輝の順です。

- `slide.tex`：編集用のLaTeXソース。
- `slide.pdf`：本編と付録をまとめた34ページの配布用PDF。
- `appendix/main.tex`：付録の編集用LaTeXソース。
- `week4.ipynb`：スライドに対応する実習ノートブック。
- `../../templates/beamer/blue-lecture-theme.tex`：共通の表紙・見出し・フォント・ページ番号設定。

元PDFではコードの多くが画像ですが、2025年度のNotebookをコード例の資料として使っています。スライドは4:3、本文12pt、コード14pt/16ptです。本文はUD デジタル 教科書体 NとArial（なければLiberation Sans）、数式はLatin Modern Math、コードはConsolas（なければLiberation Mono）を使います。

## 内容

| 本編本文ページ | 内容 |
|---|---|
| 1〜3 | 講義予定、授業リンク、Colabへノートブックを取り込む手順 |
| 4 | 自由落下の時刻・位置・速度 |
| 5〜6 | 時刻・位置リストの追加と削除、同じ添字での対応 |
| 7 | 前回の関数free_fallを使う |
| 8 | Python list・array.array・NumPy ndarrayの違い |
| 9 | ndarrayで自由落下を一括計算し、時刻点数を変える |
| 10 | 添字で同じ時刻のデータを取り出す |
| 11 | 各時刻の運動エネルギー |
| 12 | 多次元配列のshapeと行・列の添字 |
| 13 | 粒子の位置配列と行列による回転 |
| 14 | 仮想的な周期データの平均と分散 |
| 15 | 再現可能な仮想測定データの準備 |
| 16 | 物理の例で配列を使う実習 |

上の本文ページ番号は本編表紙を除いた番号です。配布PDFでは本編表紙が1ページ、表の本文は2〜17ページです。

## 付録：array.arrayとndarray

[slide.pdf](slide.pdf)が配布用PDFです。1〜17ページが本編、18〜34ページが付録です。両方の部の表紙と印刷済みページ番号を保ち、PDFしおりの「本編」と「付録：arrayとndarray」から各部へ移動できます。Notebookでも本編の直後に「付録A」を置き、同じ順序で比較を確認できます。付録単体の`appendix/main.pdf`は結合用のビルド入力として生成します。

付録では、次の11項目を扱います。

1. Python `list`、標準`array.array`、NumPy `ndarray`の違い
2. 作成方法と`typecode`・`dtype`
3. 演算子の意味
4. 標準`array`の追加・削除
5. NumPyの追加・削除と返り値
6. 多次元配列と`axis`
7. スライスのコピーとview
8. `shape`、`reshape`、転置、行列積
9. 整数配列への小数代入
10. 標準`array`とNumPy配列の相互変換
11. 自由落下計算での使い分け

## コンパイルと編集

`2026/week4`で以下を順に実行すると、配布用の`slide.pdf`を再生成できます。結合にはPythonパッケージ`pypdf`が必要です。

```sh
latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=.beamer-build/main slide.tex
latexmk -cd -lualatex -interaction=nonstopmode -halt-on-error appendix/main.tex
python3 merge_pdfs.py
```

編集するソースは本編の`slide.tex`と付録の`appendix/main.tex`です。コードを変えた場合は、対応するNotebookのセルと保存出力も更新してください。

## Notebookの使い方

[week4.ipynb](week4.ipynb)の冒頭に目次と実行手順があります。授業では本編と3問の実習を進め、付録・補足・発展は必要に応じて参照します。

| 区分 | 内容 |
|---|---|
| 本編 | 自由落下、エネルギー、多次元配列、粒子の回転、周期の模擬測定、実習3問 |
| 付録A | `array.array`と`ndarray`の詳しい比較。配布PDFの付録と対応 |
| 補足B | Pythonのリスト・タプル・集合・辞書 |
| 補足C | NumPyの配列作成、ソート、スライス、条件選択、ベクトル・行列演算 |
| 発展D | `for`文での統計計算、固有値、`einsum`、ヘルプと実行時間、追加実習2問 |

本編は上から順に実行します。任意の区分から始める場合も、その区分の先頭から実行してください。補足の例は本編の時刻・位置・速度などの変数を上書きしない名前にしています。5つの解答セルは空欄のままです。

型の違いを示す3つの例では、意図した`TypeError`を捕まえてメッセージを表示し、一括実行が途中で止まらないようにしています。`?`によるヘルプは必要なときだけ実行します。実行時間の計測は短い回数に抑え、結果は実行環境によって変わることを明記しています。

説明の重複と細切れのセルを整理し、166セルから110セルにまとめました。Python 3.12.14、NumPy 2.5.4のIPython環境で49個のコード例を通して実行し、出力を保存しています。付録A・補足B・補足C・発展Dはそれぞれ初期状態からも実行を確認しました。自由落下のエネルギー、回転前後の距離、周期統計、固有値と`einsum`の計算結果を照合しています。Colab上での実行は未確認です。

## 教材の前提

中心となる例は、同じ添字で時刻と物理量を対応づけ、同じ式を複数の時刻・粒子へ適用することです。自由落下では空気抵抗を無視し、静止状態・位置x=0から下向きを正に落下させます。落下開始からの経過時間はt≥0、重力加速度g=10.0 m/s^2は教材内の近似値です。位置はm、速度はm/s、運動エネルギーはJで表し、運動エネルギーは失った位置エネルギーmgxに等しくなります。

本文8では、Pythonのlist、標準ライブラリarray.array、NumPyのndarrayの違いを説明します。ndarrayは共通dtypeを持つ多次元配列で、数値計算を要素ごとに適用できます。

周期の4値と1000個の測定値は模擬データであり、実測結果ではありません。1000個のデータの生成では、真の周期2.0 s、独立な正規誤差の標準偏差0.1 sを仮定しています。有限標本の平均・分散は理論値に完全には一致しません。seedは再現用です。

固有値の例には実対称行列を使います。外積の成分は`o_ij = b_i a_j`で、`einsum`の説明でも添字の和を明示しています。乱数は`default_rng`でseedを固定しています。`?`、`%timeit`、`%%timeit`はIPython専用です。

## 参照

- [2025年度スライド](../../2025/week4/week4.pdf)・[2025年度ノートブック](../../2025/week4/week4.ipynb)
- 『実践計算物理学』野本拓也・是常隆・有田亮太郎（共立出版）
- [共通Beamerテンプレート](../../templates/beamer/README.md)
- [Python：組み込み型](https://docs.python.org/3/library/stdtypes.html)
- [Python：arrayモジュール](https://docs.python.org/3/library/array.html)
- [Python：数値と文字列の紹介](https://docs.python.org/3/tutorial/introduction.html)
- [NumPy：初心者向けガイド](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [NumPy：array](https://numpy.org/doc/stable/reference/generated/numpy.array.html)
- [NumPy：ones](https://numpy.org/doc/stable/reference/generated/numpy.ones.html)
- [NumPy：eigh](https://numpy.org/doc/stable/reference/generated/numpy.linalg.eigh.html)
- [NumPy：var](https://numpy.org/doc/stable/reference/generated/numpy.var.html)
- [NumPy：einsum](https://numpy.org/doc/stable/reference/generated/numpy.einsum.html)
- [NumPy：random](https://numpy.org/doc/stable/reference/random/index.html)
- [参考教材：PHYS6350 Computational Physics](https://github.com/vlvovch/PHYS6350-ComputationalPhysics)
