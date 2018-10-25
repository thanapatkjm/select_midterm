from zeep import Client
from lxml import etree 
import xmlschema


client = Client('http://127.0.0.1:5000/soap/Data?wsdl')
resultXMLtest = client.service.myData()
##root = etree.fromstring(resultlistfood)
##for food in root.findall('food'):
##    print("name :",food.find('name').text)
##    print("price :",food.find('price').text)
##    print("descr :",food.find('description').text.replace('\n',' '))
##    print("cal :",food.find('calories').text)
##    print()

# # print(resultXMLtest)

utf8_parser = etree.XMLParser(encoding='utf-8')
root = etree.fromstring(resultXMLtest.encode('utf-8'), parser=utf8_parser)
for info in root.findall('item'):
 print("date :",info.find('Name').text)
 print("id :",info.find('StudentID').text)
 print("hobby :",info.find('Hobby').text)
 print()

