from werkzeug.wsgi import DispatcherMiddleware
from spyne.server.wsgi import WsgiApplication
from spyne import Iterable, Integer, Unicode, srpc, rpc, Application, DateTime
from spyne.model.primitive import String, Double, Integer, Time, AnyXml, AnyDict, Float
from spyne.model.complex import ComplexModel, XmlAttribute
from spyne.model.complex import Array
from spyne.service import ServiceBase
from spyne.protocol.soap import Soap11
from spyne.protocol.xml import XmlDocument
from spyne.protocol.http import HttpRpc
import xml.etree.ElementTree as et

import socket

from flask import Flask

app = Flask(__name__)

class StudentFormat(ComplexModel):
    __namespace__= "studentform"
    Name = String
    ID = String
    Hobby1 = String
    Hobby2 = String
    Hobby3 = String

class AirFormat(ComplexModel):
    __namespace__ = "airform"
    airNumber = String
    airDate = String
    airTemp = String
    airHumid = String

##class PostmanFormat(ComplexModel):
##    __namespace__ = "postform"
    
class Data(ServiceBase):
    
    @srpc(_returns=AirFormat)
    def airData():
        airxml=[]
        listAir_no = ['1','2','3','4','5']
        listAir_date = ['11/12/18','11/12/18','11/12/18','11/12/18','11/12/18',]
        listAir_temp = ['32','30','34','35','36']
        listAir_humid = ['12','13','14','15','16']
        for i in listAir_no:
            airInfo = [listAir_no[i],listAir_date[i],listAir_temp[i],listAir_humid[i]]
##            airxml.append(airInfo)
            return airInfo
    
    @srpc(_returns=StudentFormat)
    def studentData():
        studentName = 'Thanapat Klayjamlang'
        studentID = '5801012630084'
        studentHobby = ['Game','Fishing','Playing Guitar']
        myInfo = [studentName,studentID,studentHobby[0],studentHobby[1],studentHobby[2]]
        return myInfo

    @rpc(_returns=String)
    def postmanOffice(ctx):
        customer = []
        customer_name = ['A','B','C']
        customer_address = ['127 soi3','128 soi5','213 soi 28/7']
        customer_weight = ['2','20','5']
        for i in range(3):
            tempData={}
            tempData['Name'] = customer_name[i]
            tempData['Address'] = customer_address[i]
            tempData['Weight'] = customer_weight[i]
            customer.append(tempData)
        customerXml = dicttoxml.dicttoxml(customer)
        return customerXml
        
    
application = Application([Data],
    tns='spyne.examples.cctv',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
# SOAP services are distinct wsgi applications, we should use dispatcher
# middleware to bring all as together
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/soap': WsgiApplication(application)
})
if __name__ == '__main__':
    app.run()
    s = socket.socket()
    s.bind(('127.0.0.1' , 5000))
    s.listen()
    while True:
        c, addr = s.accept()
        print('Got connection from', addr)
        print(c.recv(1024))
        c.close()
    
