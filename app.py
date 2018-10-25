from werkzeug.wsgi import DispatcherMiddleware
from spyne.server.wsgi import WsgiApplication
from spyne import Iterable, Integer, Unicode, srpc, Application, String
from spyne.service import ServiceBase
from spyne.protocol.soap import Soap11

from flask import Flask

app = Flask(__name__)

class studentInformation(ServiceBase):
    

    @srpc(_returns=Iterable(String))
    def CCTVList():
        yield 'CCTV01'
        yield 'CCTV02'
        yield 'CCTV03'

application = Application([studentInformation],
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
