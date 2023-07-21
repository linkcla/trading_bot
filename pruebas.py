import ccxt
import time

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


while True:
    valor = exchange.fetch_ticker('BTC/USDT')
    print(valor['last'])
    time.sleep(5)
