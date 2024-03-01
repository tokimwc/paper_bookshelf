# Paper Bookshelf for Mattermost


このPythonスクリプトは、指定されたキーワードに基づいてarXivから最新の論文を検索し、その要約を生成して、Mattermostチャンネルに投稿する自動化ツールです。特にコンピュータサイエンスの分野（人工知能、機械学習、ロボティクス）に焦点を当てています。

## 機能

- arXivから指定したキーワードに関連する最新の論文を検索。
- 論文の要約を生成。
- Mattermostチャンネルに論文の要約を自動投稿。

## 事前に必要な設定

1. MattermostサーバーのURL、ボットのアクセストークン、投稿先チャンネルIDを環境変数に設定する。
2. 依存ライブラリをインストールする。

### 環境変数

以下の環境変数を設定してください。

- `YOUR_MATTERMOST_URL`: MattermostサーバーのURL。
- `YOUR_BOT_ACCESS_TOKEN`: Mattermostボットのアクセストークン。
- `YOUR_CHANNEL_ID`: 投稿先のチャンネルID。

## 前提条件

1. [Python](https://www.python.org/downloads/)をインストールします.
2. このリポジトリを複製(Git clone)またはダウンロードします。
3. Run `pip install -r requirements.txt` を実行して必要なパッケージをインストールします。.

# 使用方法

1. 必要な環境変数`.env`を設定します。
2. スクリプトを実行します。

```sh
python paper_letter_lm.py
```

# スクリプトの構成
- main(): メインの実行関数。キーワードリストに基づいて各キーワードごとにjob()関数を呼び出します。
- job(keyword, paper_hash, is_debug): 指定されたキーワードでarXivを検索し、見つかった論文の要約をMattermostに投稿します。
- get_summary(result): arXivの検索結果から論文の要約を生成します。
- post_to_mattermost(mattermost_channel_id, message): 指定されたMattermostチャンネルにメッセージを投稿します。

# 注意事項
- このスクリプトは、OpenAI API を直接使用する代わりに、LM Studio の AI ツール機能を利用して、HTTP サーバー機能経由で LLM を実行します。これにより、言語モデルをローカル サーバー上で直接操作できるようになり、完全にオフラインの機能がサポートされます。
- 実際のデプロイメントでは、LM Studio はアプリ内チャット UI または OpenAI 互換ローカル サーバーを通じてモデルの使用を容易にします。HuggingFace リポジトリから互換性のあるモデル ファイルをダウンロードし、アプリのホームページから新しい注目すべき LLM を直接探索できます。

LM Studio の詳細については、[LM Studio](https://lmstudio.ai/)を参照してください。