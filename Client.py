from zeep import Client
from lxml import etree 
import xmlschema
import socket


client = Client('http://127.0.0.1:5000/soap/Data?wsdl')
## myInfo
##resultXMLtest = client.service.myData()
##utf8_parser = etree.XMLParser(encoding='utf-8')
##root = etree.fromstring(resultXMLtest.encode('utf-8'), parser=utf8_parser)
##for info in root.findall('item'):
##     print("date :",info.find('Name').text)
##     print("id :",info.find('StudentID').text)
##     print("hobby :",info.find('Hobby').text)
##     print()

postman = client.service.postmanOffice()
utf8_parser = etree.XMLParser(encoding='utf-8')
root = etree.fromstring(postman.encode('utf-8'), parser=utf8_parser)
for pInfo in root.findall('item'):
##    print("date :",pInfo.find('Name').text)
    detect = pInfo.find('Name')
    if(detect=='B'):
        print(1)
        s = socket.socket()
        s.connect(('localhost',5000))
        s.sendall('B is received'.encode('utf-8'))
        s.close()


