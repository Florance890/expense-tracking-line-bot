#test_webhook.py
'''import requests

print("開始執行 test_webhook.py")

data = {
    "message": "午餐 120"
}

url = "http://127.0.0.1:5000/webhook"

print("準備傳送：", data)

try:
    response = requests.post(
        url,
        json=data
    )

    print("傳送完成")
    print("狀態碼：", response.status_code)
    print("回應：", response.text)

except Exception as e:
    print("發生錯誤：", e)'''

import requests

data = {
    "message": "午餐 120"
}

response = requests.post(
    "http://127.0.0.1:5000/webhook",
    json=data
)

print(response.text)