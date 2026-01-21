"""Discord Bot APIを使用してメッセージを取得するモジュール"""
import asyncio
from datetime import datetime, timedelta, timezone
from typing import Optional, List
import discord
from config import Config


class DiscordMessageFetcher:
    """Discord Bot APIでメッセージを取得するクラス"""

    def __init__(self):
        # Intentsの設定（メッセージ内容の読み取りに必要）
        intents = discord.Intents.default()
        intents.message_content = True

        self.client = discord.Client(intents=intents)
        self.messages: List[str] = []
        self.fetch_complete = asyncio.Event()

    async def fetch_messages(self, hours_ago: int = 24) -> Optional[str]:
        """指定時間内のメッセージを取得"""

        @self.client.event
        async def on_ready():
            print(f"Bot接続完了: {self.client.user}")

            try:
                # チャンネルを取得
                channel = self.client.get_channel(Config.DISCORD_CHANNEL_ID)

                if channel is None:
                    # キャッシュにない場合はfetchで取得
                    channel = await self.client.fetch_channel(Config.DISCORD_CHANNEL_ID)

                if channel is None:
                    print(f"エラー: チャンネルID {Config.DISCORD_CHANNEL_ID} が見つかりません")
                    self.fetch_complete.set()
                    return

                print(f"チャンネル取得: #{channel.name}")

                # 指定時間前からのメッセージを取得
                cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours_ago)

                message_count = 0
                async for message in channel.history(after=cutoff_time, limit=100):
                    # Bot自身のメッセージは除外
                    if message.author.bot:
                        continue

                    content = message.content.strip()
                    if content:
                        # タイムスタンプとユーザー名を含める
                        timestamp = message.created_at.strftime("%Y-%m-%d %H:%M")
                        formatted = f"[{timestamp}] {message.author.display_name}:\n{content}"
                        self.messages.append(formatted)
                        message_count += 1

                print(f"取得したメッセージ: {message_count}件")

            except discord.Forbidden:
                print("エラー: チャンネルへのアクセス権限がありません")
            except discord.NotFound:
                print(f"エラー: チャンネルID {Config.DISCORD_CHANNEL_ID} が見つかりません")
            except Exception as e:
                print(f"エラー: {e}")
            finally:
                self.fetch_complete.set()

        # Botを起動してメッセージを取得
        async def run_bot():
            try:
                await self.client.start(Config.DISCORD_BOT_TOKEN)
            except discord.LoginFailure:
                print("エラー: Botトークンが無効です")
                self.fetch_complete.set()

        # Botの起動とメッセージ取得を並行実行
        bot_task = asyncio.create_task(run_bot())

        # 取得完了を待機（タイムアウト60秒）
        try:
            await asyncio.wait_for(self.fetch_complete.wait(), timeout=60)
        except asyncio.TimeoutError:
            print("警告: メッセージ取得がタイムアウトしました")

        # Botを終了
        await self.client.close()

        # メッセージを時系列順に並べ替えて結合
        if not self.messages:
            return None

        # 古い順にソート（リストは新しい順で追加されている）
        self.messages.reverse()

        return "\n\n---\n\n".join(self.messages)

    async def fetch_moshin_analysis(self) -> Optional[str]:
        """moshin朝分析のメッセージを取得"""
        content = await self.fetch_messages(hours_ago=24)

        if not content:
            print("メッセージが見つかりませんでした")
            return None

        print(f"取得完了: {len(content)}文字")
        return content


async def main():
    """テスト実行"""
    fetcher = DiscordMessageFetcher()
    content = await fetcher.fetch_moshin_analysis()

    if content:
        print("=" * 50)
        print(content[:500] if len(content) > 500 else content)
        print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
