import telebot, requests
from bs4 import BeautifulSoup
from time import sleep
#enter apikey from https://etherscan.io
apikey = ""
# enter public ETH Address for scan internal transaction
public_address = ""

channel_id = ""
tel_token = ""
bot = telebot.TeleBot(tel_token, parse_mode=None)

url = "https://api.etherscan.io/api?module=account&action=txlistinternal&address={0}&apikey={1}".format(public_address,apikey)
check_hash_url = "https://etherscan.io/tx/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

#test url

# print(url)
hash_list = []
r = requests.get(url)
r = r.json()
#print(r)
result = r['result']
tx_hash=""
while (True):
    r = requests.get(url)
    r = r.json()
    result = r['result']
    if r['status'] == '1':
        for i in range(0,len(result)):
           # print(result[i])
           tx_hash = result[i]
           tx_hash = tx_hash['hash']
           check_hash = tx_hash in hash_list
           if check_hash == True:
               #print("check hash is : ", tx_hash)
               pass
           else :
               hash_list.append(tx_hash)
               req = requests.get(check_hash_url+tx_hash,headers=headers)
               
               if (req.status_code !=200) :
                   
                   
                   #print("req error ")
                   pass
               else:
                   
                
                   soup = BeautifulSoup(req.text, 'html.parser')
                   token_id = soup.find_all('span',{"class":"hash-tag text-truncate"})
                   token_id = token_id[0]
                   token_id = token_id['title']
                   #print(token_id)
                   price_value = soup.find("span",{"id":"ContentPlaceHolder1_spanValue"})
                   price_value = price_value.text
                   price_value = price_value.strip()
                   price_value = price_value.split("  ")
                   eth_value = price_value[0]
                   dollar_value = price_value[1]
                   hyper_link = "<a href='{}'>Check TxId</a>".format(check_hash_url+tx_hash)
                   p = '''💰 New order 💰 💵\nPrice = {0} | {1} 💵\n⛓ {2}⛓\n💎Number ofe of  sold : {3} 💎'''.format(eth_value,dollar_value,hyper_link,token_id)
                   #print(p)
                   bot.send_message(channel_id,text=p,parse_mode='html')

    else : 
        r = requests.get(url)
        r = r.json()
        result = r['result']
    sleep(20)
    
