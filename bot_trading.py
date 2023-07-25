import ccxt
import pandas_ta as ta
import pandas as pd


exchange = ccxt.okx({
    'apiKey': '29328226-77af-4516-a7b7-d132e61c4f78',
    'secret': 'EBE9305A0C3336DC3DF0227C5058074E',
    'password': 'TestTrading2023#'
})

bars = exchange.fetch_ohlcv('BTC/USDT', timeframe='1d', limit=300)

df = pd.DataFrame(
    bars, columns=['times', 'open', 'hight', 'low', 'close', 'volume'])

# ------------------------ INDICATORS -----------------------
adx = round(ta.adx(df['hight'], df['low'], df['close']), 2)

rsi = round(ta.rsi(df['close']), 2)

ema55 = round(ta.ema(df['close'], 55), 2)

ema200 = round(ta.ema(df['close'], 200), 2)

atr = round(ta.atr(df['hight'], df['low'], df['close'], 14), 2)

sqz = round(ta.squeeze(df['hight'], df['low'], df['close']), 2)


# Concatenate

#  FORMAT:   times   open   hight   low   close   volume   ADX_14   DMP_14   DMN_14   RSI_14   ATRr_14   SQZ_20_2.0_20_1.5   SQZ_ON   SQZ_OFF   SQZ_NO   EMA_55   EMA_200
df = pd.concat([df, adx, rsi, atr, sqz, ema55, ema200], axis=1)
print(df)
actualCandle = df.iloc[-1]
oneCandle = df.iloc[-2]
twoCandle = df.iloc[-3]
threeCandle = df.iloc[-4]

# ------------------------ FUNCTIONS ------------------------

buy_requisits = {
    "val1": False,
    "val2": False,
    "val3": False
}
# val1 -Tendencia alcista o cruce de medias hacia arriba
# val2 -Movimiento con fuerza bajista perdiendo fuerza o movimiento con fuerza alcista
# val3 -Señal de compra de SQZ

sell_requisits = {
    "val1": False
}


def get_trend():
    if actualCandle['EMA_55'] > actualCandle['EMA_200']:
        up_trend = True
    elif actualCandle['EMA_55'] <= actualCandle['EMA_200']:
        up_trend = False
    buy_requisits['val1'] = up_trend


def get_movement_force():
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

    buy_requisits['val2'] = bullish_mov_getting_force or barish_mov_lossing_force


def get_info_sqz():
    """ This function returns the buy/sell signals of the Squeeze momentum indicator of Lazy Bear"""
    if threeCandle['SQZ_20_2.0_20_1.5'] < 0:
        if threeCandle['SQZ_20_2.0_20_1.5'] > twoCandle['SQZ_20_2.0_20_1.5'] & twoCandle['SQZ_20_2.0_20_1.5'] < oneCandle['SQZ_20_2.0_20_1.5']:
            buy_requisits['val3'] = True

    elif threeCandle['SQZ_20_2.0_20_1.5'] > 0:
        if threeCandle['SQZ_20_2.0_20_1.5'] < twoCandle['SQZ_20_2.0_20_1.5'] & twoCandle['SQZ_20_2.0_20_1.5'] > oneCandle['SQZ_20_2.0_20_1.5']:
            sell_requisits['val1'] = True


def get_stop_loss(long_or_short):
    """ This function calculates and returns the price of the stop loss """
    # long == true
    if (long_or_short):
        return round(oneCandle['close'] - (oneCandle['ATRr_14']*1.5), 2)
    else:
        return round(oneCandle['close'] + (oneCandle['ATRr_14']*1.5), 2)


def get_take_profit(long_or_short):
    """ This function calculates and returns the price of the take profi """
    # long == true
    if (long_or_short):
        return round(oneCandle['close'] + (oneCandle['ATRr_14']*1.5), 2)
    else:
        return round(oneCandle['close'] - (oneCandle['ATRr_14']*1.5), 2)


def buy():
    buy = True
    for i in buy_requisits.values():
        buy &= i

    if buy:
        # buy
        # put_stop_loss = get_stop_loss(True)
        # put_take profit = get_take_profit(True)
        pass


def sell():
    sell = True
    for i in sell_requisits.values():
        sell &= i
    # if sell & position_with_profit:
    #     sell


# def get_over_s_s():
#     output = '30 < RSI < 70'
#     if actualCandle['RSI_14'] > 70:
#         output = 'Sobre compra (venta)'
#     if actualCandle['RSI_14'] < 30:
#         output = 'Sobre venta (compra)'
#     return output


# ------------------- INDICADORES CON MÁS INFO -----------------------

# def get_trend():
#     output = ''
#     if actualCandle['EMA_55'] > actualCandle['EMA_200']:
#         output += 'Tendencia alcista'
#     elif actualCandle['EMA_55'] < actualCandle['EMA_200']:
#         output += 'Tendencia bajista'
#     else:
#         # ema55 == ema200
#         if oneCandle['EMA_55'] > oneCandle['EMA_200']:
#             output += 'Cruce de medias hacia arriba'
#         else:
#             output += 'Cruce de medias hacia abajo'
#     return output


# def get_movement_force():
#     MIN_FORCE = 23
#     output = ''
#     if oneCandle['ADX_14'] > MIN_FORCE:
#         output += 'Movimiento con fuerza'
#         if oneCandle['DMP_14'] > oneCandle['DMN_14']:
#             output += ' alcista'
#         else:
#             output += ' bajista'

#         if oneCandle['ADX_14'] <= twoCandle['ADX_14']:
#             output += ' perdiendo fuerza'
#     else:
#         output += 'Movimiento sin fuerza'
#         if oneCandle['DMP_14'] > oneCandle['DMN_14']:
#             output += ' alcista'
#         else:
#             output += ' bajista'

#         if oneCandle['ADX_14'] <= twoCandle['ADX_14']:
#             output += ' perdiendo fuerza'
#     return output


# def get_info_sqz():
#     """ This function returns the buy/sell signals of the Squeeze momentum indicator of Lazy Bear"""
#     if threeCandle['SQZ_20_2.0_20_1.5'] < 0:
#         if threeCandle['SQZ_20_2.0_20_1.5'] > twoCandle['SQZ_20_2.0_20_1.5'] & twoCandle['SQZ_20_2.0_20_1.5'] < oneCandle['SQZ_20_2.0_20_1.5']:
#             return 'SQZ buy signal'

#     elif threeCandle['SQZ_20_2.0_20_1.5'] > 0:
#         if threeCandle['SQZ_20_2.0_20_1.5'] < twoCandle['SQZ_20_2.0_20_1.5'] & twoCandle['SQZ_20_2.0_20_1.5'] > oneCandle['SQZ_20_2.0_20_1.5']:
#             return 'SQZ sell signal'
#     else:
#         return 'No buy/sell info'
