"""LINE Messaging APIを使用して通知を送信するモジュール"""
import requests
from datetime import datetime
from config import Config


class LineSender:
    """LINE Messaging APIを使用したメッセージ送信クラス"""

    API_URL = "https://api.line.me/v2/bot/message/push"
    MAX_MESSAGE_LENGTH = 5000

    def __init__(self):
        self.token = Config.LINE_CHANNEL_ACCESS_TOKEN
        self.user_id = Config.LINE_USER_ID

    def send(self, text: str) -> bool:
        """LINEにメッセージを送信する"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        # 5000文字を超える場合は分割送信
        chunks = self._split_message(text)

        for chunk in chunks:
            payload = {
                "to": self.user_id,
                "messages": [
                    {"type": "text", "text": chunk}
                ],
            }

            try:
                response = requests.post(self.API_URL, headers=headers, json=payload)
                if response.status_code != 200:
                    print(f"LINE送信エラー: {response.status_code} {response.text}")
                    return False
            except Exception as e:
                print(f"LINE送信エラー: {e}")
                return False

        print("LINE送信成功")
        return True

    def _split_message(self, text: str) -> list:
        """メッセージを5000文字以内に分割する"""
        if len(text) <= self.MAX_MESSAGE_LENGTH:
            return [text]

        chunks = []
        while text:
            if len(text) <= self.MAX_MESSAGE_LENGTH:
                chunks.append(text)
                break
            # 改行位置で分割を試みる
            split_pos = text.rfind("\n", 0, self.MAX_MESSAGE_LENGTH)
            if split_pos == -1:
                split_pos = self.MAX_MESSAGE_LENGTH
            chunks.append(text[:split_pos])
            text = text[split_pos:].lstrip("\n")

        return chunks

    def send_summary(self, summary: str) -> bool:
        """要約をLINEに送信する"""
        today = datetime.now().strftime("%Y/%m/%d")
        message = f"【moshin朝分析】{today} の要約\n\n{summary}"
        return self.send(message)


def main():
    """テスト実行"""
    sender = LineSender()
    result = sender.send_summary("テスト送信です。LINE Messaging API連携のテスト。")
    print(f"送信結果: {'成功' if result else '失敗'}")


if __name__ == "__main__":
    main()
