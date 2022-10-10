# RSI_bot

This script bot was developed in order to find RSI divergence signals.
Here are some examples on 1h timeframe:

![Screenshot_7](https://user-images.githubusercontent.com/109293615/194825117-2b954753-cf2a-41ff-8bcd-b309abc70506.jpg) ![image](https://user-images.githubusercontent.com/109293615/194826297-7bde2002-0d08-421b-8415-2fdd91f42b60.png) ![image](https://user-images.githubusercontent.com/109293615/194826368-59a980e4-e659-4410-85fb-74ff04dea9d2.png)

# Setup 
- pip install all the packages 

```
import websocket
import json
import talib
import numpy
import pandas as pd
import telebot
import datetime
from binance.client import *
```
- set up the kline interval

```
url = 'wss://fstream.binance.com:443/ws/' + TICKER + '@kline_1m'
data = client.futures_klines(symbol=TICKER.upper(), interval=Client.KLINE_INTERVAL_1MINUTE, limit=100)
```

- set up constants for ticker and indicators

```
TICKER = 'ethusdt'
RSI_PERIOD = 14
MA_PERIOD = 9
ATR_PERIOD = 14
TREND_FLOAT = 1
RSI_DIFFERENCE_FLOAT = 0.3
TREND_SPECTATING_LENGTH = 30
```

- set up Telegram and Binance API keys

```
bot = telebot.TeleBot('525628497:AAGkHGl-R8_K3sdsfCXvTq66VXLaj2cKZKeU')
client = Client('RLA6HRcBhlJKoXQVu6Z3UCRsTZCwqxdsfkNSEGdmwzV1BquwEu4G5A5Jc094Ak2J',
                'VpFxCLaKJWCXEBz17gdRuOfaZ1M6z8sdfOFIqP1mAjkIeSe2AlMX1bLU6cyUIE3S')
```

# Conditions for Buy signal

Accordind to the strategy for buy signal we need 3 conditions to be True.

1. Checking the previous low
2. Cheking that current low price is less than previous low price
3. Checking the RSI divergence between previous and current low


if three of them == True:  we get a buy signal

```
bool1 = previous_low < str(previous_low_MA - TREND_FLOAT * previous_low_ATR)
bool2 = current_low < previous_low
bool3 = current_RSI - previous_low_RSI > RSI_DIFFERENCE_FLOAT
```
Each time the candle closes bot is checking for a buy signal and we are getting the output.

![image](https://user-images.githubusercontent.com/109293615/194832898-f4454fd8-b335-4c6b-958f-5e16f2da6abc.png)

# do not hesitate to contact me if you face any problem
My contacts: 
Telegram: @upworkacc1
Skype: live:rejmis360


