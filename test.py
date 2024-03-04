import pyupbit
import telegram
import asyncio


access = "F74eqP4c6tuRUBffX6WBk2zK01Ixdr7eHx2wfT6E"          # 본인 값으로 변경
secret = "6KX486aQJlcu4VZrOkAulao2RM4r1prxHtLt8Jvs"          # 본인 값으로 변경

async def send_message(message):
    token = "6793842218:AAEq_mk2fPh6LWZ5WUvrmXih1hJeaOH8rkQ"
    chat_id = 5253588138

    bot = telegram.Bot(token)
    await bot.sendMessage(chat_id, message)


upbit = pyupbit.Upbit(access, secret)



print(upbit.get_balance("KRW-BTC"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회


chat_id = 5253588138

message = "보유현금 : "  + str(upbit.get_balance("KRW")) + "원"

asyncio.run(send_message(message))
