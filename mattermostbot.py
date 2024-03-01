import requests
import os
# from dotenv import load_dotenv

# .envファイルを読み込む
# load_dotenv()

# 環境変数からMattermostの設定を取得
mattermost_url = os.environ.get("YOUR_MATTERMOST_URL")
mattermost_token = os.environ.get("YOUR_BOT_ACCESS_TOKEN")
mattermost_channel_id = os.environ.get('YOUR_CHANNEL_ID')

message = "Hello, Mattermost!"

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
    # 成功した場合、レスポンスのステータスコードは201です
    if response.status_code == 201:
        print("メッセージが正常に投稿されました。")
    else:
        #エラー情報を含む例外を投げます
        raise Exception(f"Mattermostへの投稿に失敗しました。ステータスコード: {response.status_code}, エラーメッセージ: {response.text}")

# この関数を使ってMattermostにメッセージを送信
post_to_mattermost(mattermost_channel_id, message)
