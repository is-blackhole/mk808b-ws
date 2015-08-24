import sys

from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.websocket import WebSocketServerFactory

from twisted.python import log
from twisted.internet import reactor

log.startLogging(sys.stdout)


class TronsmartStickerServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onMessage(self, payload, isBinary):
        self.sendMessage(payload, isBinary)

if __name__ == '__main__':
    factory = WebSocketServerFactory()
    factory.protocol = TronsmartStickerServerProtocol
    reactor.listenTCP(9000, factory)
    reactor.run()
