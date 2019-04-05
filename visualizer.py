import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import json
import time
import numpy as np

style.use('seaborn')

fig = plt.figure(figsize=(16,8))
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,1,2)


def animate(i):
    try:
        with open('/Users/sunyan/blockchainAnalytics/Order Book Reconstruction/simpleOrderBook.json', 'r') as f:
            order_data = json.load(f)

        current_time = order_data['time']
        product_id = order_data['product_id']
        best_bids = order_data['best_bids']
        best_asks = order_data['best_asks']
        spreads = order_data['spreads']
        mid_prices = order_data['mid_prices']


        if len(spreads) >= 2000:
            ax1.clear()
            ax1.plot(best_bids[-2000:], label = 'best bid')
            ax1.plot(best_asks[-2000:], label = 'best ask')
            ax1.plot(mid_prices[-2000:], label = 'mid price')
            ax1.legend()
            ax2.clear()
            ax2.plot(spreads[-2000:], label = 'ask-bid spread')
            ax2.legend()
        else:
            ax1.clear()
            ax1.plot(best_bids, label = 'best bid')
            ax1.plot(best_asks, label = 'best ask')
            ax1.plot(mid_prices, label = 'mid price')
            ax1.legend()
            ax2.clear()
            ax2.plot(spreads, label = 'ask-bid spread')
            ax2.legend()

    # =================bid and ask plot===================

        asks = {float(k):v for k, v in order_data['asks'].items()}
        asks4plot = [(k, v) for k, v in asks.items()]
        asks4plot.sort()
        bids = {float(k):v for k, v in order_data['bids'].items()}
        bids4plot = [(k, v) for k, v in bids.items()]
        bids4plot.sort(reverse=True)

        xa = [i[0] for i in asks4plot]
        ya = np.cumsum([i[1] for i in asks4plot])

        xb = [i[0] for i in bids4plot]
        yb = np.cumsum([i[1] for i in bids4plot])
        ax3.clear()
        ax3.step(xa[:60], ya[:60], color = 'b', where='pre', label='asks')
        ax3.vlines(x=xa[0], ymin=0, ymax = ya[0], color='b', linestyle = '-', linewidth=0.2)
        ax3.step(xb[:60], yb[:60], color = 'r', where='post', label='bids')
        ax3.vlines(x=xb[0], ymin=0, ymax = yb[0], color='r', linestyle = '-', linewidth=0.2)
        ax3.set_xlim([xb[:60][-1], xa[:60][-1]])
        # ax3.step(xa, ya, color = 'b', where='pre', label='asks')
        # ax3.vlines(x=xa[0], ymin=0, ymax = ya[0], color='b', linestyle = '-', linewidth=0.2)
        # ax3.step(xb, yb, color = 'r', where='post', label='bids')
        # ax3.vlines(x=xb[0], ymin=0, ymax = yb[0], color='r', linestyle = '-', linewidth=0.2)
        # ax3.set_xlim([xb[-1], xa[-1]])
        ax3.legend()

    except:
        time.sleep(0.25)
        print('Waiting....')


    fig.suptitle(product_id + '  ' + current_time)


# with open('/Users/sunyan/blockchainAnalytics/Order Book Reconstruction/simpleOrderBook.json', 'r') as f:
#     data = json.load(f)
# print data['asks']

ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
# asks = {float(k):v for k, v in data['asks'].items()}
# # print asks
# plt.bar(asks.keys(), asks.values())
# plt.show()
