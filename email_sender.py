"""メール送信モジュール"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime
from config import Config


class EmailSender:
    """Gmail SMTPを使用したメール送信クラス"""

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    def __init__(self):
        self.sender = Config.GMAIL_ADDRESS
        self.password = Config.GMAIL_APP_PASSWORD
        self.recipient = Config.RECIPIENT_EMAIL

    def send(self, subject: str, body: str) -> bool:
        """メールを送信する"""
        try:
            # メールメッセージを作成
            msg = MIMEMultipart("alternative")
            msg["Subject"] = Header(subject, "utf-8")
            msg["From"] = self.sender
            msg["To"] = self.recipient

            # HTMLメール本文
            html_body = self._create_html_body(body)

            # プレーンテキストとHTMLの両方を添付
            part1 = MIMEText(body, "plain", "utf-8")
            part2 = MIMEText(html_body, "html", "utf-8")

            msg.attach(part1)
            msg.attach(part2)

            # SMTPサーバーに接続して送信
            with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(msg)

            print(f"メール送信成功: {self.recipient}")
            return True

        except Exception as e:
            print(f"メール送信エラー: {e}")
            return False

    def _create_html_body(self, text: str) -> str:
        """テキストをHTMLメール形式に変換"""
        # 改行をHTMLの改行タグに変換
        html_content = text.replace("\n", "<br>")

        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px 10px 0 0;
            text-align: center;
        }}
        .content {{
            background: #f9f9f9;
            padding: 20px;
            border: 1px solid #ddd;
            border-top: none;
            border-radius: 0 0 10px 10px;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #888;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>moshin朝分析 要約</h1>
        <p>{datetime.now().strftime('%Y年%m月%d日')}</p>
    </div>
    <div class="content">
        {html_content}
    </div>
    <div class="footer">
        <p>このメールは自動送信されています</p>
    </div>
</body>
</html>
"""

    def send_summary(self, summary: str) -> bool:
        """要約メールを送信する"""
        today = datetime.now().strftime("%Y/%m/%d")
        subject = f"【moshin朝分析】{today} の要約"
        return self.send(subject, summary)


def main():
    """テスト実行"""
    sender = EmailSender()

    test_summary = """
本日のポイント:
- NY市場は上昇基調
- ハイテク株に注目
- 押し目買いを狙う展開

注目銘柄:
- AAPL: 決算発表後の動きに注目
- NVDA: AI関連で引き続き強い

総評:
全体的にリスクオンの展開。
ただしFOMCを控えて上値は限定的か。
"""

    result = sender.send_summary(test_summary)
    print(f"送信結果: {'成功' if result else '失敗'}")


if __name__ == "__main__":
    main()
