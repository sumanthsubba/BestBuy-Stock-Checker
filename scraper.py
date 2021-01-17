import os
from twilio.rest import Client
import requests
import json
import boto3
from datetime import datetime
import time

URL = 'https://www.bestbuy.ca/ecomm-api/availability/products?accept=application%2Fvnd.bestbuy.standardproduct.v1%2Bjson&accept-language=en-CA&locations=940%7C928%7C972%7C627%7C639%7C224%7C975&postalCode=K1T4E1&skus=14962185'
# URL = 'https://www.bestbuy.ca/ecomm-api/availability/products?accept=application%2Fvnd.bestbuy.standardproduct.v1%2Bjson&accept-language=en-CA&locations=967%7C962%7C252%7C651%7C970%7C968%7C82%7C969%7C251%7C84%7C978%7C971%7C674%7C663%7C681&postalCode=H8S1B3&skus=13863133'

headers = {
'authority': 'www.bestbuy.ca',
'pragma': 'no-cache',
'cache-control': 'no-cache',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
'accept': '*/*',
'sec-fetch-site': 'same-origin',
'sec-fetch-mode': 'cors',
'sec-fetch-dest': 'empty',
'referer': 'https://www.bestbuy.ca/en-ca/product/playstation-5-console-online-only/14962185',
# 'referer': 'https://www.bestbuy.ca/en-ca/product/hp-15-6-laptop-silver-intel-core-i5-1035g1-512gb-ssd-8gb-ram-windows-10/13863133',
'accept-language': 'en-US,en;q=0.9'
}

def main():
    quantity = 0
    attempt = 0
 
    while (quantity < 1):
        response = requests.get(URL, headers=headers)
        response_formatted = json.loads(response.content.decode('utf-8-sig').encode('utf-8'))
 
        quantity = response_formatted['availabilities'][0]['shipping']['quantityRemaining']
 
        if (quantity < 1):
            #Out Of stock
            print('Time=' + str(datetime.now()) + "- Attempt=" + str(attempt) + '\n' + headers['referer'])
            attempt += 1
            time.sleep(5)
        else:
            print('In stock! Quantity=' + str(quantity) + '\n' + headers['referer'])
            publish(quantity)
 
 
def publish(quantity):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    response = "It's in stock! Quantity=" + str(quantity) + '\n' + headers['referer']

    message = client.messages \
                .create(
                     body=response,
                     from_='+13433127859',
                     to='+----------'
                 )

    print(message.sid)
    # arn = 'arn:aws:sns:us-east-1:119667922984:InStockTopic'
    # sns_client = boto3.client(
    #     'sns',
    #     aws_access_key_id='',
    #     aws_secret_access_key='',
    #     region_name='us-east-1'
    # )
 
#     response = sns_client.publish(TopicArn=arn, Message='Its in stock! Quantity=' + str(quantity))
#     print(response)
 
main()