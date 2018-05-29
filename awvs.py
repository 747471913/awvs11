__author__ = '盖春桦'
import requests
import json
import time
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning


ul='https://jjbond-pc:3443/'
apikey='1986ad8c0a5b3df4d7028d5f3c06e936c4052ee0c02384e538706fafc49843915'
headers = {"X-Auth":apikey,"content-type": "application/json"}
targets=[]
i=0
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)#tingzhiyanzheng
#获取初始状态将已扫描过的url获取
#创建一个target，判断是否已经扫描过
#对该target进行扫描
#获取target的扫描状态
#如果扫描结束则进行下一个

def get_scan():
    targets=[]
    uri='api/v1/scans'
    print('[*]start awvs')
    try:
        re=requests.get(ul+uri,headers=headers,timeout=30,verify=False)
        result=json.loads(re.content.decode("utf-8"))
        for result in result['scans']:
            targets.append(result['target']['address'])
        return list(set(targets))
    except ZeroDivisionError as e:
        print("except:", e)
        # print('[*]error start awvs')
        # time.sleep(3)
        exit()



def create_target(url):
    uri='api/v1/targets'
    data = {"address":url,"description":url,"criticality":"20"}
    try:
        re=requests.post(ul+uri,data=json.dumps(data),headers=headers,timeout=30,verify=False)
        result=json.loads(re.content.decode("utf-8"))
        return result['target_id']
    except:
        print('[*]创建target失败')



def get_profile_id(i):
    uri='api/v1/scanning_profiles'
    try:
        re=requests.get(ul+uri,headers=headers,timeout=30,verify=False)
        results=json.loads(re.content.decode("utf-8"))
        for result in results["scanning_profiles"]:
            pass
        return result["profile_id"]
    except:
        print('[*]获取profile_id失败')


def creat_profile_id(a):
    b=int(a[-12:])
    b=b+1
    b=str(b)
    length=len(str(b))
    l=list(a)
    for i in range(length):
        index=0-length+i
        l[index]=b[i]
    a = ''.join(l)
    return a

def scan_target(url):
    uri='api/v1/scans'
    target_id=create_target(url)
    #profile_id=get_profile_id(url)
    #profile_id=creat_profile_id(profile_id)
    data = {"target_id":target_id,"profile_id":"11111111-1111-1111-1111-111111111112","schedule": {"disable": False,"start_date":None,"time_sensitive": False}}
    try:
        re=requests.post(ul+uri,data=json.dumps(data),headers=headers,timeout=30,verify=False)
        print('[*]start sacn:',url)
    except:
        print('[*]扫描失败')

def get_target_status(url):
    uri='api/v1/scans'
    try:
        re=requests.get(ul+uri,headers=headers,timeout=30,verify=False)
        results=json.loads(re.content.decode("utf-8"))
        for result in results['scans']:
            if url in result['target']['address']:
                scan_id=result['scan_id']
        #print (scan_id)
        re=requests.get(ul+uri+'/'+scan_id,headers=headers,timeout=30,verify=False)
        results = json.loads(re.content.decode("utf-8"))
        status = results['current_session']['status']
        print (status)
        return status
    except:
        print('[*]获取扫描状态失败')

def start_baidu(keyword):
    targets=get_scan()
    lastpage=0
    nextpage=''
    url='https://www.baidu.com/s?wd={keyword}'.format(keyword=keyword)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    while lastpage!=1:
        lastpage=1
        re=requests.get(url,headers=headers)
        soup=BeautifulSoup(re.text,'html.parser')
        for i in soup.find_all('a',class_='n'):
            if i!=[]:
                nextpage=i.get('href')
                lastpage=0
        sps=soup.find_all('h3')
        for uri in sps:
            try:
                newurl=uri.find('a').get('href')
                re=requests.get(newurl,timeout=5,verify=False)
                #获得host
                tar='http://'+re.url.split('//')[1].split('/')[0]
                if 'baidu' not in tar:
                    if tar in targets:
                        print('[*]repeat')
                        continue
                    print(tar)
                    scan_target(tar)
                    while True:
                        status = get_target_status(tar)
                        if status =='completed':
                            break
                        time.sleep(30)

            except:
                continue
        url='https://www.baidu.com'+nextpage


if __name__ == '__main__':
    keyword='inurl:php?id=1'
    #利用百度批量
    start_baidu(keyword)





