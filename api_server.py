"""FastAPI サーバー - iOSショートカットからのトリガー用"""
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse

from config import Config
from discord_fetcher import DiscordFetcher
from summarizer import Summarizer
from line_sender import LineSender

app = FastAPI(title="Discord Summary Bot API")


@app.post("/trigger")
def trigger_summary(x_api_key: str = Header(...)):
    """要約ジョブを実行"""
    if x_api_key != Config.API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    try:
        # 1. Discordからメッセージ取得
        fetcher = DiscordFetcher()
        content = fetcher.fetch_moshin_analysis()

        if not content:
            return JSONResponse(
                status_code=200,
                content={"status": "no_messages", "message": "メッセージが見つかりませんでした"},
            )

        # 2. Claude APIで要約
        summarizer = Summarizer()
        summary = summarizer.summarize(content)

        # 3. LINEで送信
        line_sender = LineSender()
        success = line_sender.send_summary(summary)

        if success:
            return {"status": "success", "message": "要約をLINEに送信しました", "summary_length": len(summary)}
        else:
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "LINE送信に失敗しました"},
            )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)},
        )


@app.get("/health")
def health_check():
    """ヘルスチェック"""
    return {"status": "ok"}
