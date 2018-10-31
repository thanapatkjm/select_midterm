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
import csv

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

class PostmanFormat(ComplexModel):
    __namespace__ = "postform"
    customerName = String
    customerAddr = String
    weight = Float
    status = String
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

    @srpc(String, String, Double)
    def addDestinationInfo(name, address, weight):
        destInfo = [name, address, weight, 'sending']
        with open('DeliveryInfo.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(destInfo)
        csvFile.close()

    @srpc(String)
    def destinationSent(name):
        name = "'"+name+"'"
        status = 'sent'
        all_row = []
        with open('DeliveryInfo.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if len(row) < 4:
                    continue
                data = []
                for each in row:
                    data.append(each)
                if data[0]==name:
                    data[3] = status
                all_row.append(data)
            csv_file.close()
        f = open("DeliveryInfo.csv", "w")
        f.truncate()
        f.close()

        with open('DeliveryInfo.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            for row in all_row:
                writer.writerow(row)
            csvFile.close()

    @srpc(String ,_returns=PostmanFormat)
    def transportStatus(name='None'):
        with open('DeliveryInfo.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:                
                if len(row) < 4:
                    continue
                data = []
                for each in row:
                    data.append(each)
                if data[0]==name or data[0]=="'"+name+"'":
                    return row
        
    
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
    
