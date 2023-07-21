import ccxt
import pandas_ta as ta
import pandas as pd

exchange = ccxt.okx({
    'apiKey': '29328226-77af-4516-a7b7-d132e61c4f78',
    'secret': 'EBE9305A0C3336DC3DF0227C5058074E',
    'password': 'TestTrading2023#'
})

balance = exchange.fetch_balance()
# moneda = 'USDT'
# if moneda in balance:
#     moneda_balance = balance[moneda]
#     print(f"Saldo disponible de {moneda}: {moneda_balance}")
# else:
#     print(f"No tienes {moneda} en tu cuenta.")

bars = exchange.fetch_ohlcv('BTC/USDT', timeframe = '5m', limit = 300)

df = pd.DataFrame(bars, columns=['time', 'open', 'hight', 'low', 'close', 'volume'])

print(df)

adx = ta.adx(df['hight'], df['low'], df['close'])

ema55 = ta.ema(df['close'], 10)
ema200 = ta.ema(df['close'], 200)
print(f'ema55 : {ema55}')

print(f'ema200 : {ema200}')


print(f'adx :{adx}')