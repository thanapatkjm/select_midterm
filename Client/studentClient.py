from zeep import Client, Settings
import xml.etree.ElementTree as et
import datetime

url = 'http://127.0.0.1:5000/soap/?wsdl'
settings = Settings(strict=False, xml_huge_tree=True)
client_lis = Client(url, settings=settings)
data = client_lis.service.studentData()
print(data)


