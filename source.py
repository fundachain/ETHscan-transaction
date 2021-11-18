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



# print(url)
hash_list = []
r = requests.get(url)
r = r.json()
#print(r)
result = r['result']
tx_hash=""
#print("Start while ...")
while (True):
    r = requests.get(url)
    r = r.json()
    result = r['result']
    #print("Check status...")
    if r['status'] == '1':
        for i in range(0,len(result)):
           # print("for started...")
           # print(result[i])
            tx_hash = result[i]
            tx_hash = tx_hash['hash']
            dbs_file_read = open("dbs.txt", "r")
            for i in dbs_file_read.read().split("\n"):

                hash_list.append(i)

            check_hash = tx_hash in hash_list
            if check_hash == True:
               #print("check hash is : ", tx_hash)
               pass
            else :
                dbs_file = open("dbs.txt","a")
                dbs_file.write(tx_hash+'\n')
                dbs_file.close()
            #    hash_list.append(tx_hash)
                req = requests.get(check_hash_url+tx_hash,headers=headers)
               
                if (req.status_code !=200) :
                    #print("req error ")
                    pass
                else:
                    
                   
                    #print("request is 200...")
                    soup = BeautifulSoup(req.text, 'html.parser')
                    token_id = soup.find_all('span',{"class":"hash-tag text-truncate"})
                    token_id_list = []
                    try : 
                        for i in range(0, len(token_id)):
                            token_x = token_id[i]
                            token_x = token_x['title']
                            token_id_list.append(token_x)
                            #print('for is : ',token_x)
                    except:
                        pass
                    #print(token_id)
                    x=""
                    for i in token_id_list:
                        x= x+","+i
                    x = x.strip(",")
                    #print(x)
                    price_value = soup.find("span",{"id":"ContentPlaceHolder1_spanValue"})
                    price_value = price_value.text
                    price_value = price_value.strip()

                    price_value = price_value.split(" ")
                    #print("price value : ", price_value, "type is : ",type(price_value))
                    eth_value = price_value[0]
                    dollar_value = price_value[-1]
                    hyper_link = "<a href='{}'>Check TxId</a>".format(check_hash_url+tx_hash)
                    p = '''💰 New order 💰\n 💵 Price = {0} ETH | {1} 💵\n⛓ {2}⛓\n💎 sold : {3} 💎'''.format(eth_value,dollar_value,hyper_link,x)
                    #print(p)
                    bot.send_message(channel_id,text=p,parse_mode='html')

    else : 
        r = requests.get(url)
        r = r.json()
        result = r['result']
    sleep(20)
    
