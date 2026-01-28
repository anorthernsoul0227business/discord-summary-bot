"""Discord HTTP APIを使用してメッセージを取得するモジュール"""
import re
from datetime import datetime, timedelta, timezone
from typing import Optional, List

import requests

from config import Config


class DiscordFetcher:
    """DiscordユーザートークンでAPIからメッセージを取得するクラス"""

    BASE_URL = "https://discord.com/api/v9"

    def __init__(self):
        self.token = Config.DISCORD_TOKEN
        self.channel_id = self._extract_channel_id(Config.DISCORD_CHANNEL_URL)
        self.headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
        }

    @staticmethod
    def _extract_channel_id(channel_url: str) -> str:
        """チャンネルURLからチャンネルIDを抽出"""
        match = re.search(r"/channels/\d+/(\d+)", channel_url)
        if not match:
            raise ValueError(f"無効なチャンネルURL: {channel_url}")
        return match.group(1)

    def fetch_messages(self, hours_ago: int = 24, limit: int = 100) -> Optional[str]:
        """指定時間内のメッセージを取得"""
        try:
            print(f"Discord APIからメッセージを取得中 (チャンネルID: {self.channel_id})...")
            url = f"{self.BASE_URL}/channels/{self.channel_id}/messages"
            params = {"limit": limit}

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            messages_data = response.json()
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours_ago)

            messages: List[str] = []
            for msg in messages_data:
                # タイムスタンプをパース
                msg_time = datetime.fromisoformat(msg["timestamp"])
                if msg_time < cutoff_time:
                    continue

                # Bot以外のメッセージのみ
                if msg.get("author", {}).get("bot", False):
                    continue

                username = msg.get("author", {}).get("username", "Unknown")
                content = msg.get("content", "").strip()

                if not content:
                    continue

                formatted_time = msg_time.strftime("%Y-%m-%d %H:%M")
                formatted_msg = f"[{formatted_time}] {username}:\n{content}"
                messages.append(formatted_msg)

            # 古い順にソート
            messages.reverse()

            if not messages:
                print("メッセージが見つかりませんでした")
                return None

            print(f"取得したメッセージ: {len(messages)}件")
            return "\n\n---\n\n".join(messages)

        except requests.exceptions.HTTPError as e:
            print(f"Discord APIエラー: {e}")
            if e.response is not None and e.response.status_code == 401:
                print("トークンが無効です。再取得してください。")
            elif e.response is not None and e.response.status_code == 403:
                print("このチャンネルへのアクセス権がありません。")
            return None
        except Exception as e:
            print(f"メッセージ取得エラー: {e}")
            return None

    def fetch_moshin_analysis(self) -> Optional[str]:
        """moshin朝分析のメッセージを取得"""
        content = self.fetch_messages(hours_ago=24)
        if content:
            print(f"取得完了: {len(content)}文字")
        return content
