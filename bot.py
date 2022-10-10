import websocket
import json
import talib
import numpy
import pandas as pd
import telebot
import datetime
from binance.client import *


TICKER = 'ethusdt'
RSI_PERIOD = 14
MA_PERIOD = 9
ATR_PERIOD = 14
TREND_FLOAT = 1
RSI_DIFFERENCE_FLOAT = 0.3
TREND_SPECTATING_LENGTH = 30

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
bot = telebot.TeleBot('5256286497:AAGkHGl-R8_K3s8jCXvTq66VXLaj2cKZKeU')
client = Client('RLA6HRcBhlJKoXQVu6Z3UCRsTZCwqxPDCkNSEGdmwzV1BquwEu4G5A5Jc094Ak2J',
                'VpFxCLaKJWCXEBz17gdRuOfaZ1M6z8l6KOFIqP1mAjkIeSe2AlMX1bLU6cyUIE3S')

url = 'wss://fstream.binance.com:443/ws/' + TICKER + '@kline_1m'

closes = []

data = client.futures_klines(symbol=TICKER.upper(), interval=Client.KLINE_INTERVAL_1MINUTE, limit=100)
cut_data = []
for i in data:
    i[0] = datetime.datetime.fromtimestamp(int(i[0]) / 1000).strftime('%B %#d, %Y %H:%M:%S')
    cut_data.append(i[0:6])
df = pd.DataFrame(cut_data[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
print(df)


def on_open(ws):
    print('Opened connection')
    bot.send_message('459862465', 'WEB: The bot has opened the connection')

def on_close(ws):
    print('Connection closed')
    bot.send_message('459862465', 'WEB: The bot has closed the connection')


def on_message(ws, message):
    global closes
    json_message = json.loads(message)
    # pprint.pprint(json_message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print('Candle closed at {}'.format(close))
        time_of_candle = datetime.datetime.fromtimestamp(int(candle['T']) / 1000).strftime('%B %#d, %Y %H:%M:%S')
        df.loc[df.shape[0]] = [time_of_candle, candle['o'], candle['h'], candle['l'], candle['c'], candle['v']]
        if df.count()['timestamp'] > RSI_PERIOD:
            np_close = numpy.array([float(i) for i in (df['close'].to_list())])
            np_high = numpy.array([float(i) for i in (df['high'].to_list())])
            np_low = numpy.array([float(i) for i in (df['low'].to_list())])

            rsi = talib.RSI(np_close, RSI_PERIOD)
            ma = talib.MA(np_close, MA_PERIOD)
            atr = talib.ATR(np_high, np_low, np_close, ATR_PERIOD)
            macd = talib.MACD(np_close,  fastperiod=12, slowperiod=26, signalperiod=9)
            main_dataframe = df.assign(Rsi=rsi.tolist(), MA=ma.tolist(), ATR=atr.tolist(), MACD=macd[0].tolist(),  MACD1=macd[1].tolist(),  MACD2=macd[2].tolist())
            df_sorted = main_dataframe.tail(TREND_SPECTATING_LENGTH)[:-2]
            # print(df_sorted)
            low_debug = []
            for index, row in df_sorted.iterrows():
                try:
                    if float(row['low']) < float(row['MA'] - TREND_FLOAT * float(row['ATR'])):
                        # print('True low : ' + str(index) + 'Timestamp: ' + str(row['timestamp']))
                        low_debug.append(float(row['low']))
                except Exception as err:
                    print(err)

            previous_low = str(min(low_debug))
            print('Previous low : ' + str(previous_low))
            # print(main_dataframe['low'] == previous_low)

            try:
                previous_low_index = main_dataframe.index[main_dataframe['low'] == previous_low].tolist()[0]
                print('Previous low index: ' + str(previous_low_index))
            except Exception as err:
                print(err)

            previous_low_MA = main_dataframe['MA'][previous_low_index]
            print('Previous low MA: ' + str(previous_low_MA))
            previous_low_ATR = main_dataframe['ATR'][previous_low_index]
            print('Previous low ATR: ' + str(previous_low_ATR))
            previous_low_RSI = main_dataframe['Rsi'][previous_low_index]
            print('Previous low RSI: ' + str(previous_low_RSI))
            current_low = main_dataframe['low'].tolist()[-1]
            print('Current low: ' + str(current_low))
            current_RSI = main_dataframe['Rsi'].tolist()[-1]
            print('Current RSI ' + str(current_RSI))



            # print(TREND_FLOAT)
            # print(RSI_DIFFERENCE_FLOAT)
            bool1 = previous_low < str(previous_low_MA - TREND_FLOAT * previous_low_ATR)
            bool2 = current_low < previous_low
            bool3 = current_RSI - previous_low_RSI > RSI_DIFFERENCE_FLOAT
            print('Conditions : ' + ' ' +str(bool1) + ' ' + str(bool2) + ' ' + str(bool3))
            if previous_low < str(previous_low_MA - TREND_FLOAT * previous_low_ATR) and current_low < previous_low and current_RSI - previous_low_RSI > RSI_DIFFERENCE_FLOAT:
                bot.send_message('459862465', 'We have got a buy signal!!! Timestamp is: ' + main_dataframe['timestamp'].tolist()[-1] + ' and price is '+ main_dataframe['close'].tolist()[-1])
                print('BUY BUY BUY')



ws = websocket.WebSocketApp(url, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
