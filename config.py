"""設定管理モジュール"""
import os
from typing import List
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()


class Config:
    """アプリケーション設定"""

    # Discord API設定（ユーザートークン方式）
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    DISCORD_CHANNEL_URL: str = os.getenv("DISCORD_CHANNEL_URL", "")

    # Claude API設定
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # LINE Messaging API設定
    LINE_CHANNEL_ACCESS_TOKEN: str = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
    LINE_USER_ID: str = os.getenv("LINE_USER_ID", "")

    # APIサーバー認証設定
    API_SECRET_KEY: str = os.getenv("API_SECRET_KEY", "")

    @classmethod
    def validate(cls) -> List[str]:
        """設定の検証を行い、不足している項目のリストを返す"""
        missing = []

        if not cls.DISCORD_TOKEN:
            missing.append("DISCORD_TOKEN")
        if not cls.DISCORD_CHANNEL_URL:
            missing.append("DISCORD_CHANNEL_URL")
        if not cls.ANTHROPIC_API_KEY:
            missing.append("ANTHROPIC_API_KEY")
        if not cls.LINE_CHANNEL_ACCESS_TOKEN:
            missing.append("LINE_CHANNEL_ACCESS_TOKEN")
        if not cls.LINE_USER_ID:
            missing.append("LINE_USER_ID")

        return missing
