import pyupbit
import requests


access = "F74eqP4c6tuRUBffX6WBk2zK01Ixdr7eHx2wfT6E"          # 본인 값으로 변경
secret = "6KX486aQJlcu4VZrOkAulao2RM4r1prxHtLt8Jvs"          # 본인 값으로 변경
myToken = "xoxb-6733632510181-6759388351872-1hcuvLH1VKRtewUcUZpaPWTM"
myChannel = "#bitcoinautotrade"

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )


upbit = pyupbit.Upbit(access, secret)
post_message(myToken, myChannel, "4444")



print(upbit.get_balance("KRW-BTC"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회
