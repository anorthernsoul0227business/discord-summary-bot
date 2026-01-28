"""Discord moshin朝分析 自動要約Bot メインスクリプト"""
from datetime import datetime

from config import Config
from discord_fetcher import DiscordFetcher
from summarizer import Summarizer
from line_sender import LineSender


def run_summary_job():
    """メッセージ取得→要約→LINE送信のジョブ"""
    print(f"\n{'='*50}")
    print(f"ジョブ開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")

    fetcher = DiscordFetcher()
    summarizer = Summarizer()
    line_sender = LineSender()

    try:
        # 1. Discordからメッセージを取得（API経由）
        print("\n[1/3] Discordからメッセージを取得中...")
        content = fetcher.fetch_moshin_analysis()

        if not content:
            print("エラー: メッセージを取得できませんでした")
            return False

        print(f"取得完了: {len(content)}文字")

        # 2. Claude APIで要約
        print("\n[2/3] メッセージを要約中...")
        summary = summarizer.summarize(content)
        print(f"要約完了: {len(summary)}文字")

        # 3. LINEで送信
        print("\n[3/3] LINEに送信中...")
        success = line_sender.send_summary(summary)

        if success:
            print("\n完了: 要約をLINEに送信しました")
        else:
            print("\nエラー: LINE送信に失敗しました")
            return False

    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False

    print(f"\n{'='*50}")
    print(f"ジョブ終了: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    return True


def main():
    """エントリーポイント"""
    print("Discord moshin朝分析 自動要約Bot")
    print("=" * 40)

    # 設定を検証
    missing = Config.validate()
    if missing:
        print("エラー: 以下の設定が不足しています:")
        for item in missing:
            print(f"  - {item}")
        print("\n環境変数または.envファイルを確認してください。")
        exit(1)

    print(f"送信先: LINE (User ID: {Config.LINE_USER_ID[:8]}...)")
    print("=" * 40)

    success = run_summary_job()
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
