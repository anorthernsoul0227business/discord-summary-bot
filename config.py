"""設定管理モジュール"""
import os
from typing import List
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()


class Config:
    """アプリケーション設定"""

    # Discord Bot設定
    DISCORD_BOT_TOKEN: str = os.getenv("DISCORD_BOT_TOKEN", "")
    DISCORD_CHANNEL_ID: int = int(os.getenv("DISCORD_CHANNEL_ID", "0"))

    # Claude API設定
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Gmail設定
    GMAIL_ADDRESS: str = os.getenv("GMAIL_ADDRESS", "")
    GMAIL_APP_PASSWORD: str = os.getenv("GMAIL_APP_PASSWORD", "")
    RECIPIENT_EMAIL: str = os.getenv("RECIPIENT_EMAIL", "")

    @classmethod
    def validate(cls) -> List[str]:
        """設定の検証を行い、不足している項目のリストを返す"""
        missing = []

        if not cls.DISCORD_BOT_TOKEN:
            missing.append("DISCORD_BOT_TOKEN")
        if not cls.DISCORD_CHANNEL_ID:
            missing.append("DISCORD_CHANNEL_ID")
        if not cls.ANTHROPIC_API_KEY:
            missing.append("ANTHROPIC_API_KEY")
        if not cls.GMAIL_ADDRESS:
            missing.append("GMAIL_ADDRESS")
        if not cls.GMAIL_APP_PASSWORD:
            missing.append("GMAIL_APP_PASSWORD")
        if not cls.RECIPIENT_EMAIL:
            missing.append("RECIPIENT_EMAIL")

        return missing
