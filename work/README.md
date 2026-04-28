# データサイエンス特論 授業ノート

大分大学 データサイエンス特論の授業ノート・演習コードをまとめたリポジトリです。

---

## ファイル一覧

### 授業ノート（Jupyter Notebook）

| ファイル | タイトル | 主なテーマ |
|---|---|---|
| [class02.ipynb](class02.ipynb) | 第2回 | Python基礎・pandas・Requests |
| [class03.ipynb](class03.ipynb) | 第3回 | 情報理論・XPathスクレイピング・クローリング |
| [class04.ipynb](class04.ipynb) | 第4回 | データ可視化 |
| [class05.ipynb](class05.ipynb) | 第5回 | ベイズ推定・アソシエーション分析 |
| [class06.ipynb](class06.ipynb) | 第6回 | 自然言語処理・テキスト類似度 |
| [class07.ipynb](class07.ipynb) | 第7回 | グラフ理論・ネットワーク分析 |
| [class08.ipynb](class08.ipynb) | 第8回 | 回帰分析・最適化 |
| [class09.ipynb](class09.ipynb) | 第9回 | クラスタリング・ネットワーククラスタリング |
| [class10.ipynb](class10.ipynb) | 第10回 | 次元削減・正則化・トピックモデル |
| [class11.ipynb](class11.ipynb) | 第11回 | 単語埋め込み・グラフ埋め込み |
| [class12.ipynb](class12.ipynb) | 第12回 | ElasticSearch |
| [compoundrate.ipynb](compoundrate.ipynb) | 補足 | 複利計算シミュレーション |

### スクリプト（Python）

| ファイル | 説明 |
|---|---|
| [tabelog_crawler.py](tabelog_crawler.py) | Selenium による食べログ「大分市 ラーメン」クローラー |
| [browser_use_example.py](browser_use_example.py) | browser-use + Ollama（qwen3）による LLM Web エージェント |

---

## 各ノートの詳細

### class02.ipynb — Python・データ処理の基礎

Python とデータ分析ライブラリの基本的な使い方を確認する回。

- **pandas** の DataFrame 操作（読み込み・集計・フィルタリング）
- **Requests** を使った HTTP リクエストの基礎
- 郵便番号検索 API などの外部 API 呼び出し例

---

### class03.ipynb — 情報理論・スクレイピング・クローリング

情報理論の基礎を計算で確認したあと、Web からデータを取得する手法を演習する回。

- **自己情報量・エントロピー**（Shannon エントロピーの計算）
- **XPath** を使った HTML 解析（lxml）
- **Requests + lxml** による食べログ口コミクローラー（店舗レビューの取得）
- **BlueSky API**（atproto）を使った SNS 投稿の取得
- **ElasticSearch** を使った投稿検索・いいねランキング集計

---

### class04.ipynb — データ可視化

多変量データの分布や関係を視覚的に把握するための可視化手法を学ぶ回。

- **散布図**（matplotlib）による 2 変数の関係の確認
- **ペアプロット**（seaborn）による多変量データの一覧表示
- Iris データセットを題材に変数間の相関・分離可能性を観察

---

### class05.ipynb — ベイズ推定・アソシエーション分析

確率論的なデータ分析の 2 本柱を扱う回。

- **逐次ベイズ推定**：袋から玉を取り出す問題を例に、観測のたびに事後分布を更新
- **バッチベイズ推定**：対数尤度を使い全データを一括で推定
- **二項分布・ベータ分布**と共役事前分布の関係
- **アソシエーション分析**（mlxtend の Apriori / FP-Growth）でアイテム間の共起ルールを抽出

---

### class06.ipynb — 自然言語処理・テキスト類似度

テキストをコンピュータで扱う基礎から、文書間の類似度計算・共起ネットワークまでを扱う回。

- **分かち書き**：英語（NLTK）・日本語（Janome）の形態素解析
- **語幹化・原型化**（stemming / lemmatization）
- **Bag of Words** による文書ベクトル化
- **コサイン類似度**・TF-IDF による文書間類似度計算
- ユークリッド距離・Jaccard 係数など特徴空間の距離指標
- **共起ネットワーク**：BlueSky の万博関連投稿を形態素解析し networkx でグラフ化

---

### class07.ipynb — グラフ理論・ネットワーク分析

ネットワーク（グラフ）データの基礎理論と分析手法を扱う回。

- **隣接行列・グラフラプラシアン**の性質
- **連結成分**の抽出・直径・密度などの基本指標
- **クラスタ係数**（局所・大域）
- **ランダムグラフモデル**：Erdős-Rényi・Barabási-Albert（スケールフリー）・Watts-Strogatz（スモールワールド）
- **次数分布**のべき乗則（log-log プロット）
- **中心性指標**：次数・固有ベクトル・PageRank・媒介・近接
- **リンク予測**（Adamic/Adar 類似度）

---

### class08.ipynb — 回帰分析・最適化

機械学習の基礎となる回帰モデルとパラメータ推定の理論と実装を扱う回。

- **単回帰・重回帰**の数理：最小二乗法による解析解
- **損失関数の可視化**と最小化の直感的理解
- **勾配降下法**のスクラッチ実装（学習率の影響を確認）
- **最尤推定**：正規分布を仮定したパラメータ推定
- **PyTorch** の自動微分を使った実装
- **scikit-learn** の LinearRegression との結果比較

---

### class09.ipynb — クラスタリング・ネットワーククラスタリング

データや グラフをグループ分けする手法を幅広く扱う回。

- **K-Means**：スクラッチ実装とエルボー法・シルエット分析によるクラスタ数選択
- **階層型クラスタリング**（Ward 法などのデンドログラム）
- **DBSCAN**：密度ベースのクラスタリングと外れ値検出
- **Kernighan-Lin アルゴリズム**：グラフの 2 分割
- **Louvain 法**：モジュラリティ最大化による コミュニティ検出
- **ラベル伝播法**（同期・非同期）のスクラッチ実装

---

### class10.ipynb — 次元削減・正則化・トピックモデル

高次元データの扱い方と、過学習を抑えるための手法を学ぶ回。

- **主成分分析（PCA）**：共分散行列の固有値分解・寄与率・累積寄与率
- **SVD**（特異値分解）による行列の低ランク近似と復元
- **LDA**（潜在的ディリクレ配分法）：日本語テキストのトピックモデリング（gensim / PyMC）
- **交差検証**（k-fold）と train-test 分割
- **Ridge 回帰（L2）・Lasso 回帰（L1）**の正則化効果の比較

---

### class11.ipynb — 単語埋め込み・グラフ埋め込み

テキストとグラフを低次元ベクトル空間に埋め込む手法を扱う回。

- **Word2Vec Skip-gram**：確率モデルと SGD 更新式の導出
- **FastText**（日本語事前学習モデル）を使った単語類似度・アナロジータスク
- **t-SNE**：高次元埋め込みの 2D/3D 可視化（Swiss Roll データセット）
- **ランダムウォーク**：グラフ上の系列生成
- **Node2Vec**（PyTorch Geometric）：グラフノードの埋め込みと空手クラブネットワークへの適用

---

### class12.ipynb — ElasticSearch

ElasticSearch を使ったテキスト検索・集計の実践を扱う回。

- ES クラスタへの接続と基本的な CRUD 操作
- クエリ DSL（match / bool / range）による全文検索
- 集計（Aggregation）を使った統計処理
- インデックス設計と日本語アナライザーの設定

---

### compoundrate.ipynb — 複利計算シミュレーション（補足資料）

データサイエンスの文脈における数値シミュレーションの例題として複利を扱う補足ノート。

- 固定給与 vs 複利運用の資産推移比較
- 成長率（1% / 5% など）を変えたシナリオの可視化
- 時間経過に伴う指数的成長の直感的な把握

---

## tabelog_crawler.py — 食べログクローラー

**class03** の requests + lxml を使ったスクレイピング演習を発展させた Selenium ベースのクローラー。

```
食べログ「大分市 ラーメン」を検索
  └── 検索結果（最大3ページ）から店舗URLを収集
       └── 各店舗の基本情報を取得
            └── 口コミタブ（/dtlrvwlst/）を最大3ページ巡回
                 └── レビューを収集
                      └── CSV に保存
```

**出力ファイル**

| ファイル | 内容 |
|---|---|
| `tabelog_oita_ramen_stores.csv` | 店舗情報（店名・スコア・住所・ジャンル・営業時間・予算） |
| `tabelog_oita_ramen_reviews.csv` | 口コミ（投稿者・評点・タイトル・本文・投稿日） |

**実行方法**

```bash
/opt/homebrew/bin/python3 tabelog_crawler.py
```

**設定変数**（スクリプト冒頭で変更可）

| 変数 | デフォルト | 説明 |
|---|---|---|
| `MAX_SEARCH_PAGES` | `3` | 検索結果の巡回ページ数 |
| `MAX_REVIEW_PAGES` | `3` | 1店舗あたりの口コミページ数 |
| `HEADLESS` | `False` | `True` でブラウザ非表示 |

---

## 環境

- Python 3.12（Homebrew）/ 3.14
- Jupyter Notebook
- 主なライブラリ：pandas / numpy / matplotlib / seaborn / scikit-learn / networkx / gensim / PyTorch / PyTorch Geometric / selenium / atproto / elasticsearch
