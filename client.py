import json
from ws4py.client.threadedclient import WebSocketClient

class Client(WebSocketClient):

    def __init__(self, url):
        WebSocketClient.__init__(self, url)
        # self.flag = 0

    def opened(self):
        req = '{"type": "subscribe","product_ids": ["BTC-USD"],"channels": \
        ["level2"]}'
        self.send(req)

    def closed(self, code, reason=None):
        print("Closed down:", code, reason)

    def received_message(self, resp):
        resp = json.loads(str(resp))

        with open("/Users/sunyan/blockchainAnalytics/Order Book Reconstruction/level2orders.json","a") as f:
                json.dump(resp,f)
                f.write("\n")
                print("Orders are being downloaded.")


if __name__ == '__main__':
    f = open("/Users/sunyan/blockchainAnalytics/Order Book Reconstruction/level2orders.json","w")
    f.truncate()
    ws = None
    try:
        ws = Client('wss://ws-feed.pro.coinbase.com')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
