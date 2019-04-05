import json
import time

class OrderBook(object):

    def __init__(self):
        self.product_id = ''
        self.asks = dict()
        self.bids = dict()
        self.best_asks = []
        self.best_bids = []
        self.mid_prices = []
        self.spreads = []
        self.time = ''

    def initial(self, base):
        asks_records = base['asks']
        bids_records = base['bids']
        for ask in asks_records:
            self.asks[float(ask[0])] = float(ask[1])
        for bid in bids_records:
            self.bids[float(bid[0])] = float(bid[1])
        self.update()

    def add(self, resp):
        self.time = resp['time']
        side = resp['changes'][0][0]
        price = float(resp['changes'][0][1])
        size = float(resp['changes'][0][2])
        if side == 'buy':
            if size == 0:
                del self.bids[price]
            else:
                self.bids[price] = size
        else:
            if size == 0:
                del self.asks[price]
            else:
                self.asks[price] = size
        self.update()


    def update(self):
        best_ask = sorted(self.asks.keys())[0]
        best_bid = sorted(self.bids.keys(), reverse=True)[0]

        # best_bid = sorted(self.bids.keys(), reverse=True)[1]

        while (self.asks[best_ask] == 0):
            del self.asks[best_ask]
            best_ask = sorted(self.asks.keys())[0]

        while (self.bids[best_bid] == 0):
            del self.bids[best_bid]
            best_bid = sorted(self.bids.keys(), reverse=True)[0]

            # best_bid = sorted(self.bids.keys(), reverse=True)[1]

        mid_price = 0.5 * (best_bid + best_ask)
        spread = best_ask - best_bid

        self.best_asks.append(best_ask)
        self.best_bids.append(best_bid)
        self.mid_prices.append(mid_price)
        self.spreads.append(spread)

    def plot(self, ax):
        ax.plot(simpleOrderBook.best_bids)
        ax.plot(simpleOrderBook.best_asks)
        ax.plot(simpleOrderBook.mid_prices)

    def output(self):
        output_dict = dict()
        output_dict['product_id'] = self.product_id
        output_dict['asks'] = self.asks
        output_dict['bids'] = self.bids
        output_dict['best_asks'] = self.best_asks
        output_dict['best_bids'] = self.best_bids
        output_dict['mid_prices'] = self.mid_prices
        output_dict['spreads'] = self.spreads
        output_dict['time'] = self.time

        json_str = json.dumps(output_dict, indent=4)
        with open('/Users/sunyan/blockchainAnalytics/Order Book Reconstruction/simpleOrderBook.json', 'w') as json_file:
            json_file.write(json_str)


if __name__ == '__main__':
    file = open("/Users/sunyan/blockchainAnalytics/Order Book Reconstruction/level2orders.json", "r")

    simpleOrderBook = OrderBook()

    count = 0
    flag = 0

    while 1:
        line = file.readline()

        if not line:
            time.sleep(0.2)
            flag += 1

            if (flag == 50):
                print("no more data.")
                break
            continue

        data = json.loads(line)

        if count == 0:
            simpleOrderBook.initial(data)
        elif count == 1:
            simpleOrderBook.product_id = data['channels'][0]['product_ids'][0]
        else:
            simpleOrderBook.add(data)

        simpleOrderBook.output()
        print(count)

        count += 1
        flag = 0
