from werkzeug.wsgi import DispatcherMiddleware
from spyne.server.wsgi import WsgiApplication
from spyne import Iterable, Integer, Unicode, srpc, Application, String, rpc
from spyne.service import ServiceBase
from spyne.protocol.soap import Soap11
from spyne.protocol.http import HttpRpc
from lxml import etree
import dicttoxml

from flask import Flask

app = Flask(__name__)

class Data(ServiceBase):
    
    @rpc(_returns=String)
    def airData(ctx):
        airInfo = []
        listAir_no = ['1', '2','3','4','5']
        listAir_date = ['11/12/18','11/12/18','11/12/18','11/12/18','11/12/18',]
        listAir_temp = ['32','30','34','35','36']
        listAir_humid = ['12','13','14','15','16']
        for i in range(5):
            tempData={}
            tempData['No'] = listAir_no[i]
            tempData['Date'] = listAir_date[i]
            tempData['Temp'] = listAir_temp[i]
            tempData['Humid'] = listAir_humid[i]
            airInfo.append(tempData)
        airXml = dicttoxml.dicttoxml(airInfo)
        return airXml
            
    
    @rpc(_returns=String)
    def myData(ctx):
        myInfo =[]
        myTempData={}
        myTempData['Name'] = 'Thanapat Klayjamlang'
        myTempData['StudentID'] = '5801012630084'
        myTempData['Hobby'] = 'Game ,Fishing ,Playing guitar'
        myInfo.append(myTempData)
        myInfoXml = dicttoxml.dicttoxml(myInfo)
        return myInfoXml

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
    a = Data()
    print(a.airData)
