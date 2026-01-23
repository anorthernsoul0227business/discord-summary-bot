"""Playwrightを使用してDiscordからメッセージを取得するモジュール"""
import asyncio
from datetime import datetime, timedelta
from typing import Optional, List
from playwright.async_api import async_playwright, Page, Browser
from config import Config


class DiscordScraper:
    """Playwrightでブラウザ自動化してDiscordメッセージを取得するクラス"""

    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def login(self) -> bool:
        """Discordにログイン"""
        try:
            print("ブラウザを起動中...")
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=True)
            self.page = await self.browser.new_page()

            print("Discordログインページに移動中...")
            await self.page.goto("https://discord.com/login")
            await self.page.wait_for_load_state("networkidle")

            # メールアドレスを入力
            print("ログイン情報を入力中...")
            email_input = self.page.locator('input[name="email"]')
            await email_input.fill(Config.DISCORD_EMAIL)

            # パスワードを入力
            password_input = self.page.locator('input[name="password"]')
            await password_input.fill(Config.DISCORD_PASSWORD)

            # ログインボタンをクリック
            login_button = self.page.locator('button[type="submit"]')
            await login_button.click()

            # ログイン完了を待機（チャンネルリストが表示されるまで）
            print("ログイン中...")
            await self.page.wait_for_selector('[class*="sidebar"]', timeout=30000)
            print("ログイン成功")
            return True

        except Exception as e:
            print(f"ログインエラー: {e}")
            return False

    async def fetch_messages(self, hours_ago: int = 24) -> Optional[str]:
        """指定時間内のメッセージを取得"""
        if not self.page:
            print("エラー: ログインしていません")
            return None

        try:
            # チャンネルに移動
            print(f"チャンネルに移動中: {Config.DISCORD_CHANNEL_URL}")
            await self.page.goto(Config.DISCORD_CHANNEL_URL)
            await self.page.wait_for_load_state("networkidle")

            # メッセージエリアが読み込まれるまで待機
            await self.page.wait_for_selector('[class*="messageContent"]', timeout=15000)

            # スクロールして過去のメッセージを読み込む
            print("メッセージを読み込み中...")
            await self._scroll_to_load_messages()

            # メッセージを取得
            messages = await self._extract_messages(hours_ago)

            if not messages:
                print("メッセージが見つかりませんでした")
                return None

            print(f"取得したメッセージ: {len(messages)}件")
            return "\n\n---\n\n".join(messages)

        except Exception as e:
            print(f"メッセージ取得エラー: {e}")
            return None

    async def _scroll_to_load_messages(self, scroll_count: int = 5):
        """スクロールして過去のメッセージを読み込む"""
        messages_container = self.page.locator('[class*="scrollerInner"]').first

        for i in range(scroll_count):
            await self.page.keyboard.press("PageUp")
            await asyncio.sleep(0.5)

    async def _extract_messages(self, hours_ago: int) -> List[str]:
        """ページからメッセージを抽出"""
        cutoff_time = datetime.now() - timedelta(hours=hours_ago)
        messages = []

        # メッセージ要素を取得
        message_elements = await self.page.locator('[id^="chat-messages-"]').all()

        for element in message_elements:
            try:
                # ユーザー名を取得
                username_elem = element.locator('[class*="username"]').first
                username = await username_elem.text_content() if await username_elem.count() > 0 else "Unknown"

                # メッセージ内容を取得
                content_elem = element.locator('[class*="messageContent"]').first
                content = await content_elem.text_content() if await content_elem.count() > 0 else ""

                # タイムスタンプを取得
                time_elem = element.locator('time').first
                timestamp_str = await time_elem.get_attribute('datetime') if await time_elem.count() > 0 else None

                if content and content.strip():
                    # タイムスタンプをパース
                    if timestamp_str:
                        try:
                            msg_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                            msg_time = msg_time.replace(tzinfo=None)

                            # 指定時間より古いメッセージはスキップ
                            if msg_time < cutoff_time:
                                continue

                            formatted_time = msg_time.strftime("%Y-%m-%d %H:%M")
                        except:
                            formatted_time = "Unknown time"
                    else:
                        formatted_time = "Unknown time"

                    formatted_msg = f"[{formatted_time}] {username}:\n{content.strip()}"
                    messages.append(formatted_msg)

            except Exception as e:
                continue

        return messages

    async def fetch_moshin_analysis(self) -> Optional[str]:
        """moshin朝分析のメッセージを取得"""
        if not await self.login():
            return None

        content = await self.fetch_messages(hours_ago=24)
        await self.close()

        if content:
            print(f"取得完了: {len(content)}文字")
        return content

    async def close(self):
        """ブラウザを閉じる"""
        if self.browser:
            await self.browser.close()
            print("ブラウザを終了しました")


async def main():
    """テスト実行"""
    scraper = DiscordScraper()
    content = await scraper.fetch_moshin_analysis()

    if content:
        print("=" * 50)
        print(content[:500] if len(content) > 500 else content)
        print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
