このシステムは、ユーザーの自然言語クエリに対して、データベース内の文章との類似度を計算し、類似度の高いデータを取得する仕組みです。

## システム構成

システムは大きく2つのコンテナで構成されています。

### Container A
アプリケーション本体が動作するコンテナです。
`main` の中で、クエリの取得、Embedding生成、データベースからのデータ取得、類似度計算、上位データの選択を行います。

### Container B
PostgreSQLが動作するデータベースコンテナです。

PostgreSQLには `DbElements` というデータが保存されています。
各 `DbElement` は以下の2つの情報を持ちます。

- `text: str`
  - 元の文章データ
- `vector: [float]`
  - その文章をEmbeddingしたベクトル

## クエリ処理の流れ

1. `main` がユーザーから検索クエリを取得する。
   - `get query`

2. 取得したクエリをEmbeddingする。
   - `embedding`
   - 結果として検索クエリを表す `DbElement` を作成する。
   - この `DbElement` には、検索クエリの文章とEmbeddingベクトルが入る。

3. PostgreSQL（Container B）から、保存されている `DbElements` を取得する。
   - 図では `fetch all datas` と表現されている。
   - データベース側には複数の `DbElements` が存在する。

4. 検索クエリの `DbElement` と、データベースから取得した `DbElements` を `calc_similarity` に渡す。

5. `calc_similarity` で、検索クエリのEmbeddingベクトルと各データのEmbeddingベクトルの類似度を計算する。

6. 類似度の計算結果を使って `pick top n` を実行する。
   - 類似度が高いデータから上位N件を選択する。
   - 最終的に、この上位N件が検索結果となる。

## データフロー

全体の流れは以下。

User Query
→ get query
→ embedding
→ Query DbElement

同時に、

PostgreSQL
→ fetch all datas
→ DbElements

そして、

Query DbElement + DbElements
→ calc_similarity
→ pick top n
→ 検索結果

## 重要な設計上のポイント

- PostgreSQLには文章そのもの（`text`）とEmbeddingベクトル（`vector`）の両方を保存する。
- 検索時には、ユーザーのクエリをEmbeddingして検索用ベクトルを作る。
- 現在の設計では、PostgreSQLから保存済みデータをすべて取得してからアプリケーション側で類似度を計算する。
- `calc_similarity` の具体的な類似度計算方法は、この図では指定されていない。
  - 例えば cosine similarity などが候補になるが、現時点では未確定として扱う。
- `pick top n` の `N` の値も、この図では指定されていない。
- Embeddingモデルについても、この図では指定されていない。