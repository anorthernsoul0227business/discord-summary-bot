"""設定管理モジュール"""
import os
from typing import List
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()


class Config:
    """アプリケーション設定"""

    # Discord ブラウザ自動化設定
    DISCORD_EMAIL: str = os.getenv("DISCORD_EMAIL", "")
    DISCORD_PASSWORD: str = os.getenv("DISCORD_PASSWORD", "")
    DISCORD_CHANNEL_URL: str = os.getenv("DISCORD_CHANNEL_URL", "")

    # Claude API設定
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # LINE Messaging API設定
    LINE_CHANNEL_ACCESS_TOKEN: str = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
    LINE_USER_ID: str = os.getenv("LINE_USER_ID", "")

    # スケジュール設定
    SCHEDULE_HOUR: int = int(os.getenv("SCHEDULE_HOUR", "9"))
    SCHEDULE_MINUTE: int = int(os.getenv("SCHEDULE_MINUTE", "0"))

    @classmethod
    def validate(cls) -> List[str]:
        """設定の検証を行い、不足している項目のリストを返す"""
        missing = []

        if not cls.DISCORD_EMAIL:
            missing.append("DISCORD_EMAIL")
        if not cls.DISCORD_PASSWORD:
            missing.append("DISCORD_PASSWORD")
        if not cls.DISCORD_CHANNEL_URL:
            missing.append("DISCORD_CHANNEL_URL")
        if not cls.ANTHROPIC_API_KEY:
            missing.append("ANTHROPIC_API_KEY")
        if not cls.LINE_CHANNEL_ACCESS_TOKEN:
            missing.append("LINE_CHANNEL_ACCESS_TOKEN")
        if not cls.LINE_USER_ID:
            missing.append("LINE_USER_ID")

        return missing
