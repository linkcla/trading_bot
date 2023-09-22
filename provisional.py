# import ccxt
import pandas_ta as ta
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# exchange = ccxt.okx({
#     'apiKey': '29328226-77af-4516-a7b7-d132e61c4f78',
#     'secret': 'EBE9305A0C3336DC3DF0227C5058074E',
#     'password': 'TestTrading2023#'
# })

# bars = exchange.fetch_ohlcv('BTC/USDT', timeframe='4h', limit=300)

btc = yf.Ticker('BTC-USD')
df = btc.history(period='1mo', interval='5m')

# df = pd.DataFrame(
#     bars, columns=['Date', 'Open', 'High', 'Low', 'Close'])
# df = pd.DataFrame(
#     bars, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
# df = df[['Date', 'Open', 'High', 'Low', 'Close']]
# print(df)
# ------------------------ INDICATORS -----------------------
adx = round(ta.adx(df['High'], df['Low'], df['Close']), 2)

rsi = round(ta.rsi(df['Close']), 2)

stochrsi = round(ta.stochrsi(df['Close']), 2)

ema55 = round(ta.ema(df['Close'], 55), 2)

ema200 = round(ta.ema(df['Close'], 200), 2)

atr = round(ta.atr(df['High'], df['Low'], df['Close'], 14), 2)

sqz = round(ta.squeeze(df['High'], df['Low'], df['Close']), 2)


# Concatenate

#  FORMAT:   Date   Open   High   Low   Close    ADX_14   DMP_14   DMN_14   RSI_14   ATRr_14   SQZ_20_2.0_20_1.5   SQZ_ON   SQZ_OFF   SQZ_NO   EMA_55   EMA_200
df = pd.concat([df, adx, atr, sqz, ema55, ema200, stochrsi, rsi], axis=1)

# ------------------------ FUNCTIONS ------------------------


def get_trend(actualCandle):
    if actualCandle['EMA_55'] > actualCandle['EMA_200']:
        up_trend = True
    else:
        up_trend = False
    return up_trend


def get_movement_force_long(oneCandle, twoCandle):
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


def get_movement_force_short(oneCandle, twoCandle):
    MIN_FORCE = 23
    barish_mov_getting_force = False
    bulish_mov_lossing_force = False

    if oneCandle['ADX_14'] > MIN_FORCE:
        if oneCandle['DMN_14'] > oneCandle['DMP_14']:
            if oneCandle['ADX_14'] > twoCandle['ADX_14']:
                barish_mov_getting_force = True
        else:
            if oneCandle['ADX_14'] <= twoCandle['ADX_14']:
                bulish_mov_lossing_force = True

    return barish_mov_getting_force or bulish_mov_lossing_force


def get_info_sqz(oneCandle, twoCandle, threeCandle):
    """ This function returns the buy/sell signals of the Squeeze momentum indicator of Lazy Bear"""

    if threeCandle['SQZ_20_2.0_20_1.5'] < 0:
        if (twoCandle['SQZ_20_2.0_20_1.5'] < oneCandle['SQZ_20_2.0_20_1.5']):
            return True, False

    elif threeCandle['SQZ_20_2.0_20_1.5'] > 0:
        if (twoCandle['SQZ_20_2.0_20_1.5'] > oneCandle['SQZ_20_2.0_20_1.5']):
            return False, True
    #      buy  , sell
    return False, False


def get_stop_loss(long_or_short, oneCandle):
    """ This function calculates and returns the price of the stop loss """
    # long == true
    if (long_or_short):
        return round(oneCandle['Close'] - (oneCandle['ATRr_14']*1.5), 2)
    else:
        return round(oneCandle['Close'] + (oneCandle['ATRr_14']*1.5), 2)


def get_take_profit(long_or_short, oneCandle):
    """ This function calculates and returns the price of the take profit """
    # long == true
    if (long_or_short):
        return round(oneCandle['Close'] + (oneCandle['ATRr_14']*1.5), 2)
    else:
        return round(oneCandle['Close'] - (oneCandle['ATRr_14']*1.5), 2)


# ------------ PATRONES DE VELAS ------------

# ---- Patrones bajistas ----

def barish_engulfing(oneCandle, twoCandle):
    if oneCandle['Open'] > twoCandle['Close'] and oneCandle['Close'] < twoCandle['Open']:
        return True
    return False


def barish_doji(oneCandle, twoCandle):
    if (oneCandle['Open'] > twoCandle['Close'] and
            abs(oneCandle['Close'] - oneCandle['Open']) <= (oneCandle['High'] - oneCandle['Low']) * 0.1):
        return True
    return False


def evening_star(oneCandle, twoCandle, threeCandle):
    if (
        oneCandle['Open'] > twoCandle['Close'] and
        twoCandle['Open'] > threeCandle['Close'] and
        oneCandle['Close'] < twoCandle['Open'] and
        twoCandle['Close'] < threeCandle['Open']
    ):
        return True
    return False


def three_black_crows(oneCandle, twoCandle, threeCandle):
    if (
        oneCandle['Open'] < twoCandle['Close'] and
        twoCandle['Open'] < threeCandle['Close'] and
        oneCandle['Close'] < twoCandle['Open'] and
        twoCandle['Close'] < threeCandle['Open']
    ):
        return True
    return False

# ---- Patrones alcistas ----


def bulish_engolfing(oneCandle, twoCandle):
    if oneCandle['Open'] < twoCandle['Close'] and oneCandle['Close'] > twoCandle['Open']:
        return True
    return False


def bullish_doji(oneCandle, twoCandle):
    if oneCandle['Open'] < twoCandle['Close'] and abs(oneCandle['Close'] - oneCandle['Open']) <= (oneCandle['High'] - oneCandle['Low']) * 0.1:
        return True
    return False


def hammer(oneCandle, twoCandle):
    if oneCandle['Open'] < twoCandle['Close'] and oneCandle['Close'] > twoCandle['Open'] and (oneCandle['Close'] - oneCandle['Low']) >= 2 * (oneCandle['Open'] - oneCandle['Close']):
        return True
    return False


def morning_star(oneCandle, twoCandle, threeCandle):
    if (
        oneCandle['Open'] < twoCandle['Close'] and
        twoCandle['Open'] < threeCandle['Close'] and
        oneCandle['Close'] > twoCandle['Open'] and
        twoCandle['Close'] > threeCandle['Open']
    ):
        return True
    return False


def three_white_soldiers(oneCandle, twoCandle, threeCandle):
    if (
        oneCandle['Open'] > twoCandle['Close'] and
        twoCandle['Open'] > threeCandle['Close'] and
        oneCandle['Close'] > twoCandle['Open'] and
        twoCandle['Close'] > threeCandle['Open']
    ):
        return True
    return False


# --------- Mirar si existe algun patron de velas activo ---------

def bulish_candle_pattern(oneCandle, twoCandle, threeCandle):
    return (bulish_engolfing(oneCandle, twoCandle) |
            bullish_doji(oneCandle, twoCandle) |
            hammer(oneCandle, twoCandle) |
            morning_star(oneCandle, twoCandle, threeCandle) |
            three_white_soldiers(oneCandle, twoCandle, threeCandle))


def barish_candle_pattern(oneCandle, twoCandle, threeCandle):
    return (barish_engulfing(oneCandle, twoCandle) |
            barish_doji(oneCandle, twoCandle) |
            evening_star(oneCandle, twoCandle, threeCandle) |
            three_black_crows(oneCandle, twoCandle, threeCandle))

# -----------------------------------------------------------


def main():
    contador = 0
    first_entry = []
    PnL = []
    win = 0
    loss = 0
    running_long_position = False
    running_short_position = False
    entry_price = -1
    stop_loss = -1
    take_profit = -1

    x = []
    y = []
    y200 = []
    y55 = []

    for i in range(204, len(df)):

        aux_df = df.head(i + 1)

        # val1 -Tendencia alcista o cruce de medias hacia arriba
        # val2 -Movimiento con fuerza bajista perdiendo fuerza o movimiento con fuerza alcista
        # val3 -Señal de compra de SQZ

        long_requisits = {
            "val1": False,
            "val2": False,
            "val3": False,
            "val4": False,
            "val5": False
        }
        short_requisits = {
            "val1": False,
            "val2": False,
            "val3": False,
            "val4": False,
            "val5": False
        }

        actualCandle = aux_df.iloc[-1]
        oneCandle = aux_df.iloc[-2]
        twoCandle = aux_df.iloc[-3]
        threeCandle = aux_df.iloc[-4]

        long_short = get_info_sqz(oneCandle, twoCandle, threeCandle)

        # True --> bull trend;  False --> bulish trend
        trend = get_trend(actualCandle)

        # -------- LONG REQUISITS -----------
        long_requisits['val1'] = trend
        long_requisits['val2'] = get_movement_force_long(oneCandle, twoCandle)
        long_requisits['val3'] = long_short[0]
        long_requisits['val4'] = (
            actualCandle['Close'] > actualCandle['EMA_200'])
        long_requisits['val5'] = bulish_candle_pattern(
            oneCandle, twoCandle, threeCandle)

        # -------- SHORT REQUISITS ----------
        short_requisits['val1'] = not trend
        short_requisits['val2'] = get_movement_force_short(
            oneCandle, twoCandle)
        short_requisits['val3'] = long_short[1]
        short_requisits['val4'] = not (
            actualCandle['Close'] > actualCandle['EMA_200'])
        short_requisits['val5'] = barish_candle_pattern(
            oneCandle, twoCandle, threeCandle)

        # ------------------ LONG position ------------------
        # Open position
        if long_requisits['val1'] & long_requisits['val2'] & long_requisits['val3'] & long_requisits['val4'] & long_requisits['val5'] & (not running_long_position):
            running_long_position = True
            entry_price = actualCandle['Close']
            stop_loss = get_stop_loss(True, oneCandle)
            take_profit = get_take_profit(True, oneCandle)
            contador += 1
            plt.scatter(actualCandle.name,
                        actualCandle['Open'], c='purple', s=25, label='Open')
            plt.scatter(actualCandle.name, stop_loss,
                        c='red', s=25, label='Stop')
            plt.scatter(actualCandle.name, take_profit,
                        c='g', s=25, label='Profit')

        if running_long_position:

            # Check if we take stop loss
            if actualCandle['Low'] <= stop_loss:
                running_long_position = False
                loss += 1
                PnL.append((stop_loss/entry_price) - 1)

            # Check if we have a sell signal of SQZ when we are in a winning position
            # if get_info_sqz(oneCandle, twoCandle, threeCandle)[1]:
            #     actual_price = actualCandle['Close']
            #     if actual_price > entry_price:
            #         running_long_position = False
            #         win += 1
            #         PnL.append((actual_price/entry_price) - 1)

            # Check if we take take profit
            if actualCandle['High'] >= take_profit:
                running_long_position = False
                win += 1
                PnL.append((take_profit/entry_price) - 1)

        # ------------------ SHORT position ------------------
        # Open position
        if short_requisits['val1'] & short_requisits['val2'] & short_requisits['val3'] & short_requisits['val4'] & short_requisits['val5'] & (not running_short_position):
            running_short_position = True
            entry_price = actualCandle['Close']
            stop_loss = get_stop_loss(False, oneCandle)
            take_profit = get_take_profit(False, oneCandle)
            contador += 1
            plt.scatter(actualCandle.name,
                        actualCandle['Open'], c='purple', s=25, label='Open')
            plt.scatter(actualCandle.name, stop_loss,
                        c='red', s=25, label='Stop')
            plt.scatter(actualCandle.name, take_profit,
                        c='g', s=25, label='Profit')

        if running_short_position:

            # Check if we take stop loss
            if actualCandle['High'] >= stop_loss:
                running_short_position = False
                loss += 1
                PnL.append(-((stop_loss/entry_price) - 1))

            # Check if we take take profit
            if actualCandle['Low'] <= take_profit:
                running_short_position = False
                win += 1
                PnL.append(-((take_profit/entry_price) - 1))

        x.append(actualCandle.name)
        y.append(actualCandle['Open'])
        y200.append(actualCandle['EMA_200'])
        y55.append(actualCandle['EMA_55'])

    plt.plot(x, y200, linewidth=1.0, color='yellow')
    plt.plot(x, y55, linewidth=1.0, color='blue')
    plt.plot(x, y, linewidth=2.0, color='black')

    print(f'{contador=}')
    print(f'{first_entry=}')
    print(f'{PnL=}')
    print(f'% PnL {sum(PnL) * 100}')
    print(f'si operaramos con 100$ tendriamos: {100 + sum(PnL)*100}')
    print(f'{win=}')
    print(f'{loss=}')
    plt.show()


main()
