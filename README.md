# LINE Bot Test

使用 **LINE Messaging API** 與 **中央氣象署開放資料平臺 API** 製作的天氣降雨提醒 LINE Bot。

## 功能

- 輸入城市名稱，回覆該城市未來 36 小時的降雨機率。
- 若降雨機率大於 0%，會在訊息中加上 **「出門記得帶傘」** 的提醒。

## 環境需求

- Python 3.8+
- 註冊 LINE Messaging API 取得 **Channel Access Token** 與 **Channel Secret**
- 申請中央氣象署 API Key

## 安裝

1. 下載

   ```bash
   git clone https://github.com/Youjia0706/LINE-Bot-Test.git
   ```

2. 安裝套件

   ```bash
   pip install -r requirements.txt
   ```

3. 建立 `setting.json`

   ```json
   {
     "CHANNEL_ACCESS_TOKEN": "LINE Bot Access Token",
     "CHANNEL_SECRET": "LINE Bot Channel Secret",
     "CWB_API_KEY": "中央氣象署 API Key",
     "PORT": 5000
   }
   ```
