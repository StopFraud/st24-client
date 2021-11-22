import urllib.request, json, os,time,pika
import requests
cred_file="cred.txt"
def _cred(s,u,p,c):
    fh=open(cred_file,"a",encoding="utf-8")
#    fh=open(logfile,"a")
#    text=str(datetime.datetime.now())+" "+str(message)+"\r\n"
    text=s+","+u+","+p+","+c+"\r\n"
#    _log(text)
    fh.write(text)
    fh.close()
    return True

def service_check(pip):
    #2do: add json hostname to dns
    good_proxy=1
    while good_proxy==1:
#        url= urllib.request.urlopen("http://json.stopfraud.cyou:8000")
#        data = json.loads(url.read().decode())
#    print(data)

        proxies={'https':'http://'+pip}
        print(proxies)

        if good_proxy==1:            
            url= urllib.request.urlopen("http://json.stopfraud.cyou:8000")
            data = json.loads(url.read().decode())

            d1={'fingerprint':'2d30153da9f8bba89ca38b9aef1f0b46',\
                'lang':'ru',\
'last_name':'Пещерская',
'first_name':'Валерия',\
'email':'peshvarl20012@yandex.ru'\
'password':'Aa1234561',\
'gmt_timezone':'+03:00',\
'country':'RU',\
'phone''+7975458552',\
'currency_code':'EUR',\
'campaign_code':'',\
'urlParams=lang':'ru',\
'reg_from_web':'Website',\
'emailLang':'ru'}
#            d1={'_wpcf7':'5','_wpcf7_version':'5.3.2','_wpcf7_locale':'ru_RU','_wpcf7_unit_tag':'wpcf7-f5-o1','_wpcf7_container_post':'0','your-name':data["final_name"],'email-730':data["email"],'menu-326':'Россия','tel-163':data["phone_full"],'menu-48':'Открытие счёта','your-message':data["phrase"]}
            print(d1)    
            try:
                r1 = requests.post('https://trade.sm24online.com/api/users/trading-platform/register',data=d1,proxies=proxies, timeout=15)
                print (r1.text)
                print (r1.status_code)
                print ("maxi reg")
                if ('mail_sent' in r1.text):
                    good_proxy=1
                else:
                    good_proxy=0
            except Exception as e:
                print (e)
                good_proxy=0
                pass
            if good_proxy==1:
                print('trying good proxy again')
            else:
                print('proxy became bad, quit')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    service_check(body.decode("utf-8"))


RABBITMQ_SERVER=os.getenv("RABBITMQ_SERVER")
RABBITMQ_USER=os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD=os.getenv("RABBITMQ_PASSWORD")



while True:
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(RABBITMQ_SERVER,
                                       5672,
                                       '/',
                                       credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
#        channel.basic_qos(prefetch_count=1, global_qos=False)
        channel.queue_declare(queue='st24')
        channel.basic_consume(queue='st24', on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
#    except pika.exceptions.AMQPConnectionError:
#        print ("retry connecting to rabbit")
#        time.sleep(6)
    except Exception as e1:
        print (e1)
        print ("retry connecting to rabbit")
        time.sleep(6)

