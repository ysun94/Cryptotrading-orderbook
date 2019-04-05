import PriorityQueue
import pandas as pd
from Orders import LimitOrder

class OrderBook(object):

    def __init__(self):
        self.bids = PriorityQueue()
        self.asks = PriorityQueue()
        self.ask_records = dict()
        self.bid_records = dict()

    def add(self, lo):
        if lo.side == "buy":
            self.bids.push(lo)
            # heapq.heappush(self.bids, lo)
            self.order_index[ lo.order_id ] = lo
        else:
            self.asks.push(lo)
            # heapq.heappush(self.asks, lo)
            print("A new ask is added. "
                  "(" \
               "order_id: %s, quantity: %d, " \
               "broker: %s, price: %8.2f" \
               ")" % \
                (lo.order_id, lo.quantity, lo.broker, lo.price))
            self.order_index[ lo.order_id ] = lo
        self.__match()



class baseOrderBook(OrderBook):
    def __init__(self):
        OrderBook.__init__(self)
        self.ask_array = []
        self.bid_array = []
        self.sqn = 0

    def parse(self, response):
        self.ask_array = response['asks'] # [price, size, order_id]
        self.bid_array = response['bids']
        self.sqn = response['sequence']
        self.ask_array = self._tricky_ts(self.asks)
        self.bid_array = self._tricky_ts(self.bids)


    def _tricky_ts(self, array):
        for i, x in enumerate(array):
            ts = pd.to_datetime(i, unit='ms')
            x.append(ts)

    def construct(self):

        for ask in self.ask_array:
            price = float(ask[0])
            size = float(ask[1])
            order_id = ask[2]
            ts = ask[3]
            temp_order = LimitOrder(order_id, size, 'sell', ts, price) #order_id, size, side, timestamp, price
            self._add2asks(temp_order)

        for bid in self.bid_array:
            price = float(bid[0])
            size = float(bid[1])
            order_id = bid[2]
            ts = bid[3]
            temp_order = LimitOrder(order_id, size, 'buy', ts, price) #order_id, size, side, timestamp, price
            self._add2bids(temp_order)

    def _add2asks(self, ask):
        self.asks.push(ask)

    def _add2bids(self, bid):
        self.bids.push(bid)



