import ccxt
import pandas_ta as ta
import pandas as pd


exchange = ccxt.okx({
    'apiKey': '29328226-77af-4516-a7b7-d132e61c4f78',
    'secret': 'EBE9305A0C3336DC3DF0227C5058074E',
    'password': 'TestTrading2023#'
})

balance = exchange.fetch_balance()

bars = exchange.fetch_ohlcv('BTC/USDT', timeframe='5m', limit=300)

df = pd.DataFrame(
    bars, columns=['times', 'open', 'hight', 'low', 'close', 'volume'])

# indicators
adx = ta.adx(df['hight'], df['low'], df['close'])

ema55 = ta.ema(df['close'], 55)

ema200 = ta.ema(df['close'], 200)

df = pd.concat([df, adx, ema55, ema200], axis=1)

penultRow = df.iloc[-2]
lastRow = df.iloc[-1]
#  times     open    hight      low    close    volume    ADX_14     DMP_14     DMN_14        EMA_55       EMA_200


def get_movement_force():
    output = ''
    if lastRow['ADX_14'] > 23:
        output += 'Movimiento con fuerza'
        if lastRow['DMP_14'] > lastRow['DMN_14']:
            output += ' alcista'
        else:
            output += ' bajista'

        if lastRow['ADX_14'] <= penultRow['ADX_14']:
            output += ' perdiendo fuerza'

    else:
        output += 'Movimiento sin fuerza'

    return output


def get_trend():
    output = ''
    if lastRow['EMA_55'] > lastRow['EMA_200']:
        output += 'Tendencia alcista'
    elif lastRow['EMA_55'] < lastRow['EMA_200']:
        output += 'Tendencia bajista'
    else:
        # ema55 == ema200
        if penultRow['EMA_55'] > penultRow['EMA_200']:
            output += 'Cruce de medias hacia arriba'
        else:
            output += 'Cruce de medias hacia abajo'

    return output


print(get_movement_force())
print(get_trend())
