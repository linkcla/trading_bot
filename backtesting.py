# import ccxt
import pandas_ta as ta
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


class Position():
    def __init__(self, Open_price, take_profit, stop_loss, id):
        self.Open_price = Open_price
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.id = id

    def control_position(self, actual_price):
        if actual_price >= self.take_profit:
            PnL.append((self.take_profit/self.Open_price) - 1)
            win += 1
            self.delete_position()

        if actual_price <= self.stop_loss:
            PnL.append((self.stop_loss/self.Open_price) - 1)
            loss += 1
            self.delete_position()

    def Close_position(self, actual_price):
        if actual_price > self.Open_price:
            profit += (actual_price/self.Open_price) - 1
            PnL.append((actual_price/self.Open_price) - 1)
            win += 1
            self.delete_position()

    def delete_position(self):
        del positions[self.id]


positions: list[Position] = [None] * 100
PnL = []
win = 0
loss = 0


# exchange = ccxt.okx({
#     'apiKey': '29328226-77af-4516-a7b7-d132e61c4f78',
#     'secret': 'EBE9305A0C3336DC3DF0227C5058074E',
#     'password': 'TestTrading2023#'
# })

# bars = exchange.fetch_ohlcv('BTC/USDT', timeframe='4h', limit=300)

btc = yf.Ticker('BTC-USD')
df = btc.history(period='5y')
print(df)


# df = pd.DataFrame(
#     bars, columns=['Date', 'Open', 'High', 'Low', 'Close'])
# df = pd.DataFrame(
#     bars, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
df = df[['Date', 'Open', 'High', 'Low', 'Close']]
print(df)
# ------------------------ INDICATORS -----------------------
adx = round(ta.adx(df['High'], df['Low'], df['Close']), 2)

rsi = round(ta.rsi(df['Close']), 2)

ema55 = round(ta.ema(df['Close'], 55), 2)

ema200 = round(ta.ema(df['Close'], 200), 2)

atr = round(ta.atr(df['High'], df['Low'], df['Close'], 14), 2)

sqz = round(ta.squeeze(df['High'], df['Low'], df['Close']), 2)


# Concatenate

#  FORMAT:   Date   Open   High   Low   Close    ADX_14   DMP_14   DMN_14   RSI_14   ATRr_14   SQZ_20_2.0_20_1.5   SQZ_ON   SQZ_OFF   SQZ_NO   EMA_55   EMA_200
df = pd.concat([df, adx, rsi, atr, sqz, ema55, ema200], axis=1)


# ------------------------ FUNCTIONS ------------------------


def get_trend(actualCandle):
    if actualCandle['EMA_55'] > actualCandle['EMA_200']:
        up_trend = True
    elif actualCandle['EMA_55'] <= actualCandle['EMA_200']:
        up_trend = False
    return up_trend


def get_movement_force(oneCandle, twoCandle):
    MIN_FORCE = 23
    bullish_mov_getting_force = False
    barish_mov_lossing_force = False

    if oneCandle['ADX_14'] > MIN_FORCE:
        if oneCandle['DMP_14'] > oneCandle['DMN_14']:
            if oneCandle['ADX_14'] > twoCandle['ADX_14']:
                bullish_mov_getting_force = True
        else:
            if oneCandle['ADX_14'] <= twoCandle['ADX_14']:
                barish_mov_lossing_force = True

    return bullish_mov_getting_force or barish_mov_lossing_force


def get_info_sqz(oneCandle, twoCandle, threeCandle):
    """ This function returns the buy/sell signals of the Squeeze momentum indicator of Lazy Bear"""

    if threeCandle['SQZ_20_2.0_20_1.5'] < 0:
        if (threeCandle['SQZ_20_2.0_20_1.5'] > twoCandle['SQZ_20_2.0_20_1.5']) & (twoCandle['SQZ_20_2.0_20_1.5'] < oneCandle['SQZ_20_2.0_20_1.5']):
            return True, False

    elif threeCandle['SQZ_20_2.0_20_1.5'] > 0:
        if (threeCandle['SQZ_20_2.0_20_1.5'] < twoCandle['SQZ_20_2.0_20_1.5']) & (twoCandle['SQZ_20_2.0_20_1.5'] > oneCandle['SQZ_20_2.0_20_1.5']):
            return False, True

    return False, False


def get_stop_loss(long_or_short, oneCandle):
    """ This function calculates and returns the price of the stop loss """
    # long == true
    if (long_or_short):
        return round(oneCandle['Close'] - (oneCandle['ATRr_14']*1.5), 2)
    else:
        return round(oneCandle['Close'] + (oneCandle['ATRr_14']*1.5), 2)


def get_take_profit(long_or_short, oneCandle):
    """ This function calculates and returns the price of the take profi """
    # long == true
    if (long_or_short):
        return round(oneCandle['Close'] + (oneCandle['ATRr_14']*1.5), 2)
    else:
        return round(oneCandle['Close'] - (oneCandle['ATRr_14']*1.5), 2)


def buy(buy_requisits, actualCandle, oneCandle, id):

    buy = True
    for i in buy_requisits.values():
        buy &= i

    if buy:
        positions[id] = Position(actualCandle['Close'], get_take_profit(
            True, oneCandle), get_stop_loss(True, oneCandle), id)
        id += 1

    return id


def sell(sell_requisits, actualCandle):
    sell = True
    for i in sell_requisits.values():
        sell &= i

    if sell:
        for position in positions:
            if type(position) == 'Position':
                position.Close_position(actualCandle['Close'])


def main():
    id = 0
    contador = 0
    pos = []
    for i in range(283, len(df)):

        aux_df = df.head(i + 1)

        # val1 -Tendencia alcista o cruce de medias hacia arriba
        # val2 -Movimiento con fuerza bajista perdiendo fuerza o movimiento con fuerza alcista
        # val3 -Señal de compra de SQZ

        buy_requisits = {
            "val1": False,
            "val2": False,
            "val3": False
        }
        sell_requisits = {
            "val1": False
        }

        actualCandle = aux_df.iloc[-1]
        oneCandle = aux_df.iloc[-2]
        twoCandle = aux_df.iloc[-3]
        threeCandle = aux_df.iloc[-4]

        buy_requisits['val1'] = get_trend(actualCandle)
        buy_requisits['val2'] = get_movement_force(oneCandle, twoCandle)
        buy_sell = get_info_sqz(oneCandle, twoCandle, threeCandle)
        buy_requisits['val3'] = buy_sell[0]

        if (buy_requisits['val1'] == True) & (buy_requisits['val2'] == True) & (buy_requisits['val3'] == True):
            contador += 1
            pos.append(actualCandle)

        sell_requisits['val1'] = buy_sell[1]

        id = buy(buy_requisits, actualCandle, oneCandle, id)
        sell(sell_requisits, actualCandle)

        for position in positions:
            if type(position) == '__main__.Position':
                position.control_position(actualCandle['Close'])

    print(f'{contador=}')
    print(f'{pos=}')

    print(f'PnL: {PnL}')
    print(f'wins: {win}')
    print(f'losses: {loss}')

    x = pd.to_datetime(df['Date'])
    y = df['ADX_14']
    y1 = df['SQZ_20_2.0_20_1.5'] / 100
    plt.axhline(y=0)
    plt.axhline(y=23, color='r')
    plt.plot(x, y, linewidth=2.0, color='r')
    plt.plot(x, y1, linewidth=2.0)
    plt.show()


# main()
