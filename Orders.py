class Order(object):

    def __init__(self, order_id, size, side, timestamp):
        self.order_id = order_id
        self.quantity = size
        self.timestamp = timestamp
        self.side = side

    def get_order_id(self):
        return self.order_id

    def get_timestamp(self):
        return self.timestamp

    def get_side(self):
        return self.side

    def get_size(self):
        return self.size


class LimitOrder(Order):
    def __init__(self, order_id, size, side, timestamp, price):
        Order.__init__(self, order_id, size, side, timestamp)
        self.price = price

    def signed_price(self):
        if self.side == 'buy':
            return +self.price
        else:
            return -self.price

    def __lt__(self, other):
        return (self.signed_price() > other.signed_price()) \
            or (self.signed_price() == other.signed_price()
                   and self.timestamp < other.timestamp)

    def __eq__(self, other):
        return (self.price == other.price) \
            and (self.timestamp == other.timestamp)

    def __gt__(self, other):
        return not (self.__lt__(other) or self.__eq__(other))

    def __str__(self):
        return "(" \
               "order_id: %s, size: %d, " \
               "timestamp: %d, " \
               "side: %d, price: %8.2f" \
               ")" % \
               (self.order_id, self.quantity, self.timestamp, self.direction, self.price)


    def set_size(self, value):
        self.quantity = value

    def get_price(self):
        return self.price


