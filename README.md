                                                               SETUP

Following steps must be completed to get the BOT running:

1.Requesting API key and secret from your crypto exchange. 

2.Set your api key in the coresponding section of exchange as:
      apikey = your-exchange-api-key
      secret = your-binance-testnet-api-secret
      
3.Run pip install -r requirements.txt from the project root to install the required packages

### Create user configuration

**The configuration consists of the following fields:**

-   **apiKey** - Your API key generated in the exchange account setup stage.
-   **secret** - Your secret key generated in the exchange account setup stage.
-   **symbol** - This is your starting coin of choice. This should be one of the coins from your supported coin list. 
-   **exchange** - Name of the exchange you want to use.
-   **amount**  - It is the value of the coin you wanted to buy or sell.

#### Environment Variables

```
exchange=bybit
apiKey="your api key"
secret="your secret key"
defaultType=future
period=7
atr_multiplier=3
interval=10
symbol=ETH/USDT:USDT
amount=0.001
```
4.Adjust other variables in the coresponding section of exchange according to your needs such as:
    exchange_id , defaultType , environment , interval , period , atr_multiplier and symbol.

5.Run "python bot.py" to start the BOT.

                                                             DESCRIPTION

supertrend bot using python, pandas, and ccxt

Working of the bot:
                   The buy and sell signals are generated when the indicator starts plotting either on top of the closing price or below the closing price.
A buy signal is generated when the ‘Supertrend’ closes below the price, and a sell signal is generated when it closes above the closing price.

Functionality of the bot:
                         -The user can change the exchange when is required.
                         -The user can change the ammount of the coin he/she wishes to buy or sell.
                         -The user can switch in between testnet and mainnet.
The ATR formula is: 

                   “[(Prior ATR x(n-1)) + Current TR]/n” 
                   
                   where TR = max [(high − low), abs(high − previous close), abs(low – previous close)].

The supertrend indicator calculation is:

                                        Up = (high + low / 2 + multiplier  x  ATR
                                        
                                        Down = (high + low) / 2 – multiplier x ATR