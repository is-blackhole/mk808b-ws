import sys
import kivy
from kivy.app import App
from kivy.uix.label import Label
from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import WebSocketClientFactory

from kivy.support import install_twisted_reactor
install_twisted_reactor()

from twisted.python import log
from twisted.internet import reactor

__version__ = '0.1'

log.startLogging(sys.stdout)
kivy.require('1.7.2')  # replace with your current kivy version !


class MyClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        self.sendMessage(u"Hello, world from WS!".encode('utf8'))

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
            self.factory.app.print_message(payload.decode('utf8'))


class EchoFactory(WebSocketClientFactory):
    protocol = MyClientProtocol

    def clientConnectionLost(self, conn, reason):
        self.app.print_message("connection lost")

    def clientConnectionFailed(self, conn, reason):
        self.app.print_message("connection failed")


class MyApp(App):

    def build(self):
        self.connect_to_server()
        self.label = Label(text='Hello world')
        return self.label

    def connect_to_server(self):
        factory = EchoFactory("ws://127.0.0.1:9000", debug=False)
        factory.app = self
        reactor.connectTCP("127.0.0.1", 9000, factory)

    def print_message(self, msg):
        self.label.text += "\n" + msg

if __name__ == '__main__':
    MyApp().run()
