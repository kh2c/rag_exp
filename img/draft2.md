## Flow: add database

この処理は、文章データをEmbeddingし、その文章とEmbeddingベクトルをPostgreSQLに登録するための処理です。

## システム構成

システムは2つのコンテナで構成されています。

### Container A

アプリケーション本体が動作するコンテナです。
`main` の中で、文章の取得、Embedding生成、DbElementの作成を行います。

### Container B

PostgreSQLが動作するデータベースコンテナです。

PostgreSQLには `DbElements` が保存されます。
各 `DbElement` は以下のデータを持ちます。

- `text: str`
  - 登録する元の文章
- `vector: [float]`
  - 文章をEmbeddingした結果のベクトル

## データ登録の流れ

1. `main` が登録対象となる文章を取得する。
   - `get sentence`

2. 取得した文章をEmbeddingする。
   - `embedding`

3. 文章とEmbedding結果から `DbElement` を作成する。
   - `DbElement`
   - `DbElement` は少なくとも以下の情報を持つ。
     - `text: str`
     - `vector: [float]`

4. 作成した `DbElement` をContainer BのPostgreSQLへ登録する。

5. PostgreSQL側の `DbElements` にデータが保存される。

## データフロー

全体の流れは以下。

Sentence
→ get sentence
→ embedding
→ DbElement
→ PostgreSQL
→ DbElements

## 重要な設計上のポイント

- 登録時に文章をEmbeddingする。
- Embeddingしたベクトルを、元の文章とセットでDBに保存する。
- PostgreSQLに保存されるデータは `text` と `vector` の組み合わせ。
- 後の検索処理では、この保存済み `vector` を検索クエリのEmbeddingと比較する。
- Embeddingモデルについては、この図では指定されていない。
- PostgreSQLへの具体的なINSERT方法についても、この図では指定されていない。