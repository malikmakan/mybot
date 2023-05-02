import ccxt
import schedule
import os
import pandas as pd
pd.set_option('display.max_rows', None)

import warnings
warnings.filterwarnings('ignore')

from datetime import datetime
import time

exchange_id = os.environ.get('exchange')
defaultType = os.environ.get('defaultType')
environment = os.environ.get('environment', 'development')
apiKey = os.environ.get('apiKey')
secret = os.environ.get('secret')
interval = int(os.environ.get('interval'))
period = int(os.environ.get('period'))
atr_multiplier = float(os.environ.get('atr_multiplier'))
symbol = str(os.environ.get('symbol'))
amount = float(os.environ.get('amount'))


exchange = getattr(ccxt, exchange_id)({
    'apiKey': apiKey,
    'secret': secret,
})

exchange.options['defaultType'] = defaultType




def tr(data):
    data['previous_close'] = data['close'].shift(1)
    data['high-low'] = abs(data['high'] - data['low'])
    data['high-pc'] = abs(data['high'] - data['previous_close'])
    data['low-pc'] = abs(data['low'] - data['previous_close'])
    tr = data[['high-low', 'high-pc', 'low-pc']].max(axis=1)
    return tr

def atr(data, period):
    data['tr'] = tr(data)
    atr = data['tr'].rolling(period).mean()
    return atr

def supertrend(df, period=20, atr_multiplier=10):
    hl2 = (df['high'] + df['low']) / 2
    df['atr'] = atr(df, period)
    df['upperband'] = hl2 + (atr_multiplier * df['atr'])
    df['lowerband'] = hl2 - (atr_multiplier * df['atr'])
    df['in_uptrend'] = True

    for current in range(1, len(df.index)):
        previous = current - 1

        if df['close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True

        elif df['close'][current] < df['lowerband'][previous]:
            df['in_uptrend'][current] = False

        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]

            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]

            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]
        
    return df


in_position = False

def check_buy_sell_signals(df):
    global in_position
    print("checking for buy and sell signals")
    last_row_index = len(df.index) - 1
    previous_row_index = last_row_index - 1

    if not df['in_uptrend'][previous_row_index] and df['in_uptrend'][last_row_index]:
        print("changed to uptrend, buy")
        if not in_position:
            order = exchange.create_market_buy_order(symbol, amount)
            print(order)
            in_position = True
        else:
            print("already in position, nothing to do")

    if df['in_uptrend'][previous_row_index] and not df['in_uptrend'][last_row_index]:
        if in_position:
            print("changed to downtrend, sell")
            order = exchange.create_market_sell_order(symbol, amount)
            print(order)
            in_position = False
        else:
            print("You aren't in position, nothing to sell")



def run_bot():
    print(f"Fetching new bars for {datetime.now().isoformat()}")
    bars = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=100)
    df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    supertrend_data = supertrend(df, period, atr_multiplier)
    check_buy_sell_signals(supertrend_data)


schedule.every(interval).seconds.do(run_bot)


while True:
    schedule.run_pending()
    time.sleep(1)