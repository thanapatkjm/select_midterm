from zeep import Client, Settings
import xml.etree.ElementTree as et
import datetime

url = 'http://127.0.0.1:5000/soap/?wsdl'
client_lis = Client(url)
name = 'OAT'
data = client_lis.service.transportStatus(name)
print(data)
