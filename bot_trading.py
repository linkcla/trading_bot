import ccxt
import pandas_ta as ta
import pandas as pd


exchange = ccxt.okx({
    'apiKey': '29328226-77af-4516-a7b7-d132e61c4f78',
    'secret': 'EBE9305A0C3336DC3DF0227C5058074E',
    'password': 'TestTrading2023#'
})

balance = exchange.fetch_balance()

bars = exchange.fetch_ohlcv('APIX/USDT', timeframe='1d', limit=300)

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


def get_movement_force():
    output = ''
    if actualCandle['ADX_14'] > 23:
        output += 'Movimiento con fuerza'
        if actualCandle['DMP_14'] > actualCandle['DMN_14']:
            output += ' alcista'
        else:
            output += ' bajista'

        if actualCandle['ADX_14'] <= oneCandle['ADX_14']:
            output += ' perdiendo fuerza'
    else:
        output += 'Movimiento sin fuerza'
    return output


def get_trend():
    output = ''
    if actualCandle['EMA_55'] > actualCandle['EMA_200']:
        output += 'Tendencia alcista'
    elif actualCandle['EMA_55'] < actualCandle['EMA_200']:
        output += 'Tendencia bajista'
    else:
        # ema55 == ema200
        if oneCandle['EMA_55'] > oneCandle['EMA_200']:
            output += 'Cruce de medias hacia arriba'
        else:
            output += 'Cruce de medias hacia abajo'
    return output


def get_over_s_s():
    output = '30 < RSI < 70'
    if actualCandle['RSI_14'] > 70:
        output = 'Sobre compra (venta)'
    if actualCandle['RSI_14'] < 30:
        output = 'Sobre venta (compra)'
    return output


def get_stop_loss(long_or_short):
    # long == true
    if (long_or_short):
        return round(oneCandle['close'] - (oneCandle['ATRr_14']*1.5), 2)
    else:
        return round(oneCandle['close'] + (oneCandle['ATRr_14']*1.5), 2)


def get_take_profit(long_or_short):
    # long == true
    if (long_or_short):
        return round(oneCandle['close'] + (oneCandle['ATRr_14']*1.5), 2)
    else:
        return round(oneCandle['close'] - (oneCandle['ATRr_14']*1.5), 2)


# def get_info_sqz():
