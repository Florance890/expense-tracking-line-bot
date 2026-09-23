'''from flask import Flask,request

app = Flask(__name__)

@app.route("/")
def home():
    return "記帳 Bot 正常運作！"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    print("收到資料：")
    print(data)

    return "OK"

if __name__ == "__main__":
    app.run(debug=True) '''

from flask import Flask, request
import json
import os
import requests
from datetime import datetime

CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")

app = Flask(__name__)

# 讀取記帳資料
try:
    with open("expenses.json", "r") as file:
        expenses = json.load(file)
except FileNotFoundError:
    expenses = {}
    print("第一次使用，建立新的記帳資料")

# 顯示所有支出
def show_expenses(expenses, target_date=None):
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")

    filtered = []

    for expense in expenses:
        if expense.get("date") == target_date:
            filtered.append(expense)

    if not filtered:
        return f"📋 {target_date} 沒有支出紀錄。"

    text = f"📅 {target_date} 支出紀錄\n\n"

    for i, expense in enumerate(filtered):
        text += (
            f"{i+1}. {expense.get('time', '')} "
            f"{expense['item']} ${expense['money']}\n"
        )

    total = sum(expense["money"] for expense in filtered)

    text += f"\n💰 當日總額：${total}"

    return text
    
# 計算總支出

def get_total(expenses):
    today = datetime.now().strftime("%Y-%m-%d")

    total = sum(
        expense["money"]
        for expense in expenses
        if expense.get("date") == today
    )
    return f"💰 目前總支出：${total}"


# LINE Reply API
def reply_message(reply_token, text):
    url = "https://api.line.me/v2/bot/message/reply"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }

    data = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    print("LINE 回覆狀態：", response.status_code)
    print(response.text)

#幫助

def show_help():
    return (
        "🤖 記帳 Bot 使用說明\n\n"
        "📝 新增支出\n"
        "例如：午餐 120\n\n"
        "📋 查看紀錄\n"
        "輸入：查看\n\n"
        "💰 查看總額\n"
        "輸入：總額\n\n"
        "❓ 查看說明\n"
        "輸入：幫助"
    )

# 處理 LINE 訊息
def handle_message(message, expenses):
    message = message.strip()

    if message == "查看":
        return show_expenses(expenses)

    if message == "總額":
        return get_total(expenses)

    if message == "幫助":
        return show_help()
    
    try:
        date_obj = datetime.strptime(message, "%m/%d")

        target_date = date_obj.replace(
            year=datetime.now().year
        ).strftime("%Y-%m-%d")

        return show_expenses(expenses, target_date)

    except ValueError:
        pass

# 記帳
    result = message.split()

    if len(result) != 2:
        return( "❌ 格式錯誤！\n請輸入：品項 金額\n例如：午餐 120")


    item = result[0]

    try:
        money = int(result[1])
    except ValueError:
        return "❌ 金額請輸入數字！"

    if money <= 0:
        return "❌ 金額必須大於 0！"

    today = datetime.now().strftime("%Y-%m-%d")
    expense = {
        "date":today,
        "item": item,
        "money": money
    }

    expenses.append(expense)
    total = sum(expense["money"] for expense in expenses)

    return (
        f"✅ 記帳成功！\n\n"
        f"品項：{item}\n"
        f"金額：${money}\n\n"
        f"目前總支出：${total}"
    )

# 儲存資料
def save_expenses(expenses):
    with open("expenses.json", "w") as file:
        json.dump(expenses,
            file,
            ensure_ascii=False,
            indent=4)

# 首頁
@app.route("/")
def home():
    return "記帳 Bot 正常運作！"

# LINE Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    print("收到 LINE 資料：")
    print(data)

    if not data.get("events"):
        return "OK"

    event = data["events"][0]

    if event["type"] == "message":
        reply_token = event["replyToken"]
        message = event["message"]["text"]
        user_id = event["source"]["userId"]

        print(f"LINE User ID：{user_id}")
        print(f"LINE 訊息：{message}")

        if user_id not in expenses:
            expenses[user_id] = []

        reply_text = handle_message(
            message,
            expenses[user_id]
        )
        save_expenses(expenses)
        reply_message(
            reply_token,
            reply_text
        )

    return "OK"
    
'print(handle_message("幫助", []))'

if __name__ == "__main__":
    app.run()
