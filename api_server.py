"""FastAPI サーバー - iOSショートカットからのトリガー用"""
import threading

from fastapi import FastAPI, Header, HTTPException

from config import Config
from discord_fetcher import DiscordFetcher
from summarizer import Summarizer
from line_sender import LineSender

app = FastAPI(title="Discord Summary Bot API")


def _run_summary_job():
    """バックグラウンドで要約ジョブを実行"""
    try:
        fetcher = DiscordFetcher()
        content = fetcher.fetch_moshin_analysis()

        if not content:
            print("メッセージが見つかりませんでした")
            return

        summarizer = Summarizer()
        summary = summarizer.summarize(content)

        line_sender = LineSender()
        success = line_sender.send_summary(summary)

        if success:
            print(f"要約をLINEに送信しました ({len(summary)}文字)")
        else:
            print("LINE送信に失敗しました")

    except Exception as e:
        print(f"ジョブエラー: {e}")


@app.post("/trigger")
def trigger_summary(x_api_key: str = Header(...)):
    """要約ジョブをトリガー（即座にレスポンスを返す）"""
    if x_api_key != Config.API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    thread = threading.Thread(target=_run_summary_job)
    thread.start()

    return {"status": "accepted", "message": "要約ジョブを開始しました。完了後LINEに送信されます。"}


@app.get("/health")
def health_check():
    """ヘルスチェック"""
    return {"status": "ok"}
