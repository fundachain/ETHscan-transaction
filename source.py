import telebot, requests
from bs4 import BeautifulSoup

#enter apikey from https://etherscan.io
apikey = ""
# enter public ETH Address for scan internal transaction
public_address = ""

url = "https://api.etherscan.io/api?module=account&action=txlistinternal&address={0}&apikey={1}".format(public_address,apikey)
check_hash_url = "https://etherscan.io/tx/"
#test url

# print(url)

r = requests.get(url)
r = r.json()
#print(r)
result = r['result']
if r['status'] == '1':
    for i in range(0,len(result)):
       # print(result[i])
       tx_hash = result[i]
       tx_hash = tx_hash['hash']
       req = requests.get(check_hash_url+tx_hash)
       
