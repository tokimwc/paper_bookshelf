import datetime as dt
import os
import time
from typing import Set

import arxiv
from openai import OpenAI
import requests  
# from dotenv import load_dotenv

# .envファイルを読み込む
# load_dotenv()

# Point to the local server instead of using the API key
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

# arXivのデフォルトAPIクライアントを構築
arxiv_client = arxiv.Client()

# 環境変数からMattermostの設定を取得
mattermost_url = os.environ.get("YOUR_MATTERMOST_URL")
mattermost_token = os.environ.get("YOUR_BOT_ACCESS_TOKEN")
mattermost_channel_id = os.environ.get('YOUR_CHANNEL_ID')

# queryを用意
QUERY_TEMPLATE = "%28 ti:%22{}%22 OR abs:%22{}%22 %29 AND submittedDate: [{} TO {}]"

# 投稿するカテゴリー
CATEGORIES = {
    "cs.AI", 
    "cs.LG",
    "cs.RO"
}

SYSTEM = """
### 指示 ###
論文の内容を理解した上で重要なポイントを箇条書きで3点書いて。

### 箇条書きの制約 ###
- 最大3個
- 必ず日本語
- 箇条書き1個を50文字以内

### 対象とする論文の内容 ###
{text}

### 出力形式 ###
タイトル(和名)

- 箇条書き1
- 箇条書き2
- 箇条書き3
"""

# パラメータ
MODEL_NAME = "local-model"
TEMPERATURE = 0.25
MAX_RESULT = 10
N_DAYS = 1


def get_summary(result: arxiv.Result) -> str:
    """
    論文の要約を取得
    Args:
        result: arXivの検索結果
    Returns:
        message: 要約
    """
    text = f"title: {result.title}\nbody: {result.summary}"
    cnt = 0
    while True:
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}],
                temperature=TEMPERATURE,
                max_tokens=2000,
            )
            break
        except Exception as e:
            time.sleep(20)
            cnt += 1
            # 3回失敗したらエラーを吐く
            if cnt == 3:
                raise e

    time.sleep(5)
    summary = response.choices[0].message.content
    title_en = result.title
    title, *body = summary.split("\n")
    body = "\n".join(body)
    date_str = result.published.strftime("%Y-%m-%d %H:%M:%S")
    message = f"発行日: {date_str}\n{result.entry_id}\n{title_en}\n{title}\n{body}\n"

    return message


# Mattermostにメッセージを投稿する関数
def post_to_mattermost(mattermost_channel_id: str, message: str):
    """Mattermostの特定のチャンネルにメッセージを送信するための関数"""
    headers = {
        "Authorization": f"Bearer {mattermost_token}",
        "Content-Type": "application/json",
    }
    data = {
        "channel_id": mattermost_channel_id,
        "message": message,
    }
    response = requests.post(mattermost_url, headers=headers, json=data, verify=False)
    if response.status_code != 201:
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        raise Exception("Mattermostへの投稿に失敗しました")

# 論文の要約を取得し、Mattermostに投稿する
def job(keyword: str, paper_hash: Set[str], is_debug: bool = False) -> Set[str]:
    today = dt.datetime.today() - dt.timedelta(days=3)
    base_date = today - dt.timedelta(days=1)
    query = QUERY_TEMPLATE.format(keyword, keyword, base_date.strftime("%Y%m%d%H%M%S"), today.strftime("%Y%m%d%H%M%S"))
    
    search = arxiv.Search(
        query = query,
        max_results = 10 * 3,
        sort_by = arxiv.SortCriterion.SubmittedDate,
        sort_order = arxiv.SortOrder.Descending,
    )
    
    result_list = []
    for result in arxiv_client.results(search):
        if result.title in paper_hash or len(set(result.categories) & CATEGORIES) == 0:
            continue
        result_list.append(result)
        paper_hash.add(result.title)
        if len(result_list) == 5:
            break
    
    if len(result_list) == 0:
        post_to_mattermost(mattermost_channel_id, f"{'=' * 40}\n{keyword}に関する論文は有りませんでした！\n{'=' * 40}")
    else:
        post_to_mattermost(mattermost_channel_id, f"{'=' * 40}\n{keyword}に関する論文は{len(result_list)}本ありました！\n{'=' * 40}")
        
        # 各論文の要約をMattermostに投稿
        for i, result in enumerate(result_list, start=1):
            message = f"{keyword}: {i}本目\n" + get_summary(result)
            post_to_mattermost(mattermost_channel_id, message)
            time.sleep(1)  # Mattermostへの負荷軽減のための遅延

    return paper_hash

# スクリプトが直接実行された場合のメインロジック
def main():
    keyword_list = ["artificial intelligence", "machine learning", "deep learning"]
    paper_hash = set()
    for keyword in keyword_list:
        paper_hash = job(keyword, paper_hash)

if __name__ == "__main__":
    main()
