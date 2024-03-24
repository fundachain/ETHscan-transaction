import telebot, requests
# from bs4 import BeautifulSoup
from time import sleep
from config import *
from datetime import datetime
bot = telebot.TeleBot(bot_token, parse_mode=None)

# url = "https://api.etherscan.io/api?module=account&action=txlistinternal&address={0}&apikey={1}".format(public_address,etherscan_apikey)

url = "https://api.etherscan.io/api?module=account&action=txlist&address={0}&startblock=1&endblock=99999999&sort=asc&apikey={1}".format(public_address,etherscan_apikey)

def send_message(date,Token_Name,Token_value,tx_hash):
            
    hyper_link = "<a href='{}'>Check TxId</a>".format(tx_url+tx_hash)
    p = '''💰 {0} Sale! 💰\n 💵 Date = {1} Amount | {2} 💵\n⛓ {2}⛓\n💎 txid : {3} 💎'''.format(Token_Name,date,Token_value,hyper_link)
    bot.send_message(channel_id,text=p,parse_mode='html')

def req_data():
    params = {
    "module": "account",
    "action": "tokentx",
    "address": public_address,
    "sort" : "desc",
    "apikey": etherscan_apikey
    }
    return requests.get(api_endpoint, params=params)



hash_list = []
while (True):
    tx_hash=""

    response = req_data()
    response = response.json()
    result = response['result']

    
    if response['status'] == '1':
        for blocknumber_temp in range(0,len(result)):

            tx_hash = result[blocknumber_temp]
            tx_hash = tx_hash['hash']
            dbs_file_read = open("dbs.txt", "r")
            
            for db_temp in dbs_file_read.read().split("\n"):
                hash_list.append(db_temp)

            
            if tx_hash in hash_list:
               pass

            else :
                dbs_file = open("dbs.txt","a")
                dbs_file.write(tx_hash+'\n')
                dbs_file.close()
                date = datetime.fromtimestamp(int(result[blocknumber_temp]['timeStamp']))
                Token_value = int(result[blocknumber_temp]['value']) / 10**18
                Token_Name = result[blocknumber_temp]['tokenName']
                send_message(date,Token_Name,Token_value,tx_hash)
                sleep(5)

    sleep(20)
        







    
    
