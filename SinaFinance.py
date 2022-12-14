# coding=utf-8  
import urllib
import urllib.request
import time
import re
from bs4 import BeautifulSoup  


#交易提示   
url = "http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/jyts/index.phtml"  
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
soup = BeautifulSoup(response,from_encoding="GB2312")  
#print(soup)
   
lstcode =[]
tr = soup.find_all("tr",attrs={'class':"head"})
for j in tr:
    if '债券' in j.text:
        continue
    if '货币' in j.text:
        continue
    if '纯债' in j.text:
        continue
    if '大额转换' in j.text:
        continue
    if '定期定额' in j.text:
        continue
    

    if '停牌' in j.text:
        lstcode.append(j.text)
    if '上市' in j.text:
        lstcode.append(j.text)
    if '解禁' in j.text:
        lstcode.append(j.text)
    
    
    if '业绩快报' in j.text:
        lstcode.append(j.text)
    if '经营数据' in j.text:
        lstcode.append(j.text)
    if '披露季报' in j.text:
        lstcode.append(j.text)
    if '披露中报' in j.text:
        lstcode.append(j.text)
    if '披露年报' in j.text:
        lstcode.append(j.text)
    if '财务指标' in j.text:
        lstcode.append(j.text)

    if '恢复交易' in j.text:
        lstcode.append(j.text)
    if '配股' in j.text:
        lstcode.append(j.text)
    if '送股' in j.text:
        lstcode.append(j.text)
    if '转增' in j.text:
        lstcode.append(j.text)

    if '减持' in j.text:
        lstcode.append(j.text)
    if '预亏' in j.text:
        lstcode.append(j.text)
    if '立案' in j.text:
        lstcode.append(j.text)
    if '终止' in j.text:
        lstcode.append(j.text)
    if '诉讼' in j.text:
        lstcode.append(j.text)

lst_reject=[]
for code in lstcode:
    lst_reject.append(code[1:7])
    print(code[1:7],code)

print('交易提示禁止代码个数',len(lst_reject))

#限售解禁股当日上市
vc_today =time.strftime('%Y-%m-%d',time.localtime(time.time()))
url = "http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/xsjj/index.phtml?bdate={}&edate={}".format(vc_today,vc_today)
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
soup = BeautifulSoup(response,from_encoding="GB2312")  
#print(soup)

tr = soup.find_all(href=re.compile("country=stock"))
for j in tr:
    if j.text[:1] in ['3','5', '6', '9', '0']:
        lst_reject.append(j.text)
        print(j.text," 限售解禁")


#读取通达信选股导出文件
vc_today =time.strftime('%Y%m%d',time.localtime(time.time()))
fin = open("d:\\临时条件股{}.txt".format(vc_today), 'r')
for line in fin:
    try:
        line = line[:-1]
        if not line: continue
    
        if line[:1] in ['3','5', '6', '9', '0']:
            lst_reject.append(line[:6])
            print(line[:6]," 通达信文件")
        
    except:
        continue

fin.close()

#保存到rejectcode.txt
lst_reject.sort
file_object = open('d:\\rejectcode.txt', 'w')
for line in lst_reject:
    line = line +'\n'
    file_object.write(line)
file_object.flush()
file_object.close()

print('禁止代码个数',len(lst_reject))


#从全部代码过滤rejectcode
lst_allcode = []
fin = open("d:\\沪深.txt", 'r')
for line in fin:
    try:
        line = line[:-1]
        if not line: continue
    
        if line[:1] in ['3','5', '6', '9', '0']:
            line = line[:6]
            if not line in lst_reject:
                lst_allcode.append(line)
        
    except:
        continue

fin.close()

#保存所有允许代码
file_object = open('d:\\allcode.txt', 'w')
for line in lst_allcode:
    line = line +'\n'
    file_object.write(line)
file_object.flush()
file_object.close()

print('允许代码个数',len(lst_allcode))