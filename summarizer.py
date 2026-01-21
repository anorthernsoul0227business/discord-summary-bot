"""Claude APIを使用してメッセージを要約するモジュール"""
import anthropic
from config import Config


class Summarizer:
    """Claude APIを使用した要約クラス"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def summarize(self, content: str) -> str:
        """コンテンツを要約する"""
        if not content:
            return "要約するコンテンツがありません。"

        prompt = f"""以下はDiscordの「moshin朝分析」チャンネルからの投稿内容です。
この内容を日本語で簡潔に要約してください。

要約のポイント:
- 市場の重要なポイントを箇条書きで
- 今日注目すべき銘柄やセクターがあれば記載
- トレードの方向性やアドバイスがあれば記載
- 全体的な市場の見通し

投稿内容:
{content}

---

上記の内容を分かりやすく要約してください:"""

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text


def main():
    """テスト実行"""
    summarizer = Summarizer()

    test_content = """
    おはようございます。本日の朝分析です。

    昨日のNY市場は上昇して引けました。
    S&P500は+0.5%、ナスダックは+0.8%でした。

    本日の注目ポイント:
    - 決算シーズンが本格化
    - FOMCを控えて様子見ムード
    - ハイテク株に注目

    トレード戦略:
    押し目買いを狙いたい相場です。
    """

    result = summarizer.summarize(test_content)
    print("要約結果:")
    print(result)


if __name__ == "__main__":
    main()
