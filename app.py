from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import json
from weather import get_rain_chance,format_time

#讀取環境變數
with open("setting.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

channel_access_token = settings["CHANNEL_ACCESS_TOKEN"]
channel_secret = settings["CHANNEL_SECRET"]
cwb_api_key = settings["CWB_API_KEY"]
port = settings.get("PORT", 5000)
user_id = settings.get("USER_ID")

app = Flask(__name__)
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/",methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()
    rain_schedule = get_rain_chance(user_text, cwb_api_key)

    if rain_schedule:
        reply_lines = [f"{user_text} 未來降雨預報 🌧️："]
        need_umbrella = False
        for period in rain_schedule:
            start_fmt = format_time(period['start'])
            end_fmt = format_time(period['end'])
            chance = int(period['chance']) if period['chance'].isdigit() else 0
            if chance > 0:
                need_umbrella = True
            reply_lines.append(f"{start_fmt} ~ {end_fmt}：{chance}%")
        if need_umbrella:
            reply_lines.append("出門記得帶雨傘 ☔")
        reply_text = "\n".join(reply_lines)
    else:
        reply_text = "明天不會下雨"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)