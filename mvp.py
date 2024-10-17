import telegram
import asyncio
import os
import pyupbit
from dotenv import load_dotenv
load_dotenv()

access = os.getenv("UPBIT_ACCESS_KEY")
secret = os.getenv("UPBIT_SECRET_KEY")
upbit = pyupbit.Upbit(access, secret)


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
    
    # df = pyupbit.get_ohlcv("KRW-BTC", count=30, interval="day");
    df = pyupbit.get_ohlcv("KRW-BTC", count=240, interval="minute60");
    # print(df)

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

    # print(result["decision"].upper())
    # print(result["reason"])
    # my_btc = get_balance("BTC")
    # current_price = pyupbit.get_orderbook(ticker="KRW-BTC")['orderbook_units'][0]["ask_price"]
    # print("현재 1비트 금액 : ", current_price)
    # print("현재 보유 코인 : ", my_btc)
    # print("합계 : ", my_btc * current_price)
    # my_krw = get_balance("KRW")
    # print("현재 현금 : ", my_krw)

    if result["decision"] == "buy":
        my_krw = get_balance("KRW")
        buy_cost = my_krw * 0.9995
        # print("현재 현금 : ", buy_cost)
        if my_krw * 0.9995 > 5000:
            # print("구매결정")
            buy_result = upbit.buy_market_order("KRW-BTC", my_krw * 0.9995)
            asyncio.run(send_message(buy_result))
        else:
            asyncio.run(send_message("구입실패 : 5000원 미만"))
            print("구입실패 : 5000원 미만")
    elif result["decision"] == "sell":
        my_btc = get_balance("BTC")
        current_price = pyupbit.get_orderbook(ticker="KRW-BTC")['orderbook_units'][0]["ask_price"]
        # print("현재 1비트 금액  : ", current_price)
        # print("현재 재산 : ", my_btc * current_price)
        if my_btc * current_price > 5000:
            # print("판매결정")
            sell_result = upbit.sell_market_order("KRW-BTC", my_btc)
            asyncio.run(send_message(sell_result))
        else:
            asyncio.run(send_message("판매실패 : 5000원 미만"))
            print("판매실패 : 5000원 미만")        

# ai_trading()

while True:
    import time
    ai_trading()
    time.sleep(3600)