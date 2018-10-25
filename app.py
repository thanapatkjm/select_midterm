from werkzeug.wsgi import DispatcherMiddleware
from spyne.server.wsgi import WsgiApplication
from spyne import Iterable, Integer, Unicode, srpc, Application, String
from spyne.service import ServiceBase
from spyne.protocol.soap import Soap11
from spyne.protocol.http import HttpRpc
from lxml import etree
import dicttoxml

from flask import Flask

app = Flask(__name__)

class Data(ServiceBase):
    
    @srpc(_returns=Iterable(String))
    def airData():
        airInfo = []
        listAir_no = ['1', '2','3','4','5']
        listAir_date = ['11/12/18','11/12/18','11/12/18','11/12/18','11/12/18',]
        listAir_temp = ['32','30','34','35','36']
        listAir_humid = ['12','13','14','15','16']
        for i in listAir_no:
            tempData['No'] = listAir_no[i]
            tempData['Date'] = listAir_date[i]
            tempData['Temp'] = listAir_temp[i]
            tempData['Humid'] = listAir_humid[i]
            airInfo.append(tempData)
        airXml = dicttoxml.dicttoxml(airInfo)
            
    
##    @srpc(_returns=Iterable(String))
##    def myData():
####        myTempData['Name']

application = Application([Data],
    tns='spyne.examples.cctv',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
# SOAP services are distinct wsgi applications, we should use dispatcher
# middleware to bring all aps together
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/soap': WsgiApplication(application)
})

if __name__ == '__main__':
    app.run()
