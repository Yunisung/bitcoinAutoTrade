import telegram
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

access = os.getenv("UPBIT_ACCESS_KEY")
secret = os.getenv("UPBIT_SECRET_KEY")

async def send_message(message):
    #텔레그램 메세지 보내기
    token = "6793842218:AAEq_mk2fPh6LWZ5WUvrmXih1hJeaOH8rkQ"
    chat_id = 5253588138

    bot = telegram.Bot(token)
    await bot.sendMessage(chat_id=chat_id, text=message)

def get_balance(ticker):
    #잔고조회
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

asyncio.run(send_message("ai_trading start"))

def ai_trading():
    
    # 1. 업비트 차트 가져오기 (30일 일봉)
    import pyupbit
    df = pyupbit.get_ohlcv("KRW-BTC", count=30, interval="day");

    # 2. AI에게 데이터 제공하고 판단 받기
    from openai import OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": "You're a Bitcoin investing expert.\nBased on the chart data provided\nwhether to buy, sell, or hold at the moment based on the provided chart data.\nresponse in json format.\n\nResponse Example:\n{\"decision\":\"buy\", \"reason\":\"some technical reason\"}\n{\"decision\":\"sell\", \"reason\":\"some technical reason\"}\n{\"decision\":\"hold\", \"reason\":\"some technical reason\"}"
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": df.to_json()
            }
        ]
        }
    ],
    response_format={
        "type": "json_object"
    }
    )

    result = response.choices[0].message.content

    # 3. AI판단에 따라 실제로 자동매매 하기
    import json
    result = json.loads(result)

    asyncio.run(send_message(result["decision"].upper()))
    asyncio.run(send_message(result["reason"]))

    upbit = pyupbit.Upbit(access, secret)

    

    if result["decision"] == "buy":
        my_krw = upbit.get_balances("KRW")
        if my_krw * 0.9995 > 5000:
            buy_result = upbit.buy_market_order("KRW-BTC", my_krw * 0.9995)
            asyncio.run(send_message(buy_result))
        else:
            asyncio.run(send_message("구입실패 : 5000원 미만"))
    elif result["decision"] == "sell":
        my_btc = upbit.get_balances("KRW-BTC")
        current_price = pyupbit.get_orderbook(ticker="KRW-BTC")['orderbook_units'][0]["ask_price"]
        if my_btc * current_price > 5000:
            sell_result = upbit.sell_market_order("KRW-BTC", my_btc)
            asyncio.run(send_message(sell_result))
        else:
            asyncio.run(send_message("판매실패 : 5000원 미만"))        

while True:
    import time
    ai_trading()
    time.sleep(3600)