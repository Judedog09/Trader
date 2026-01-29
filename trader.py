import alpaca_trade_api as tradeapi
import time
from datetime import datetime
import sys

# --- CONFIGURATION ---
API_KEY = "PKJ6UV4G4PKYHMVZZFNFH77BNJ"
SECRET_KEY = "44GM1kfatyhB8wAvo3moUZqb7xRFUhYS4gaX1ZCqYNn8"
BASE_URL = "https://paper-api.alpaca.markets" 

SYMBOL = "TSLA"
QTY = 5

# Initialize API
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

def run_trader():
    # flush=True forces the terminal to show the text immediately
    print(f"--- BOT ATTEMPTING START AT {datetime.now().strftime('%H:%M:%S')} ---", flush=True)
    
    try:
        print("Checking connection to Alpaca...", flush=True)
        account = api.get_account()
        print(f"CONNECTED! Account Status: {account.status} | Balance: ${account.cash}", flush=True)
    except Exception as e:
        print(f"!!! CONNECTION ERROR: {e}", flush=True)
        return

    print(f"Monitoring: {SYMBOL}", flush=True)
    print("------------------------------------------", flush=True)

    while True:
        try:
            # Fetching data
            bars = api.get_bars(SYMBOL, tradeapi.TimeFrame.Minute, limit=20).df
            
            if bars.empty:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] No data received. Is the market open?", flush=True)
                time.sleep(30)
                continue

            current_price = bars['close'].iloc[-1]
            sma = bars['close'].mean()
            
            # Check Position
            try:
                api.get_position(SYMBOL)
                holding = "YES"
            except:
                holding = "NO"

            # Dashboard print
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] PRICE: ${current_price:<8.2f} | SMA: ${sma:<8.2f} | HOLDING: {holding}", flush=True)

            # Strategy
            if current_price < (sma * 0.998) and holding == "NO":
                print(">>> SIGNAL: BUY", flush=True)
                api.submit_order(symbol=SYMBOL, qty=QTY, side='buy', type='market', time_in_force='gtc')
            
            elif current_price > (sma * 1.002) and holding == "YES":
                print(">>> SIGNAL: SELL", flush=True)
                api.submit_order(symbol=SYMBOL, qty=QTY, side='sell', type='market', time_in_force='gtc')

        except Exception as e:
            print(f"!!! RUNTIME ERROR: {e}", flush=True)

        time.sleep(60)

if __name__ == "__main__":
    run_trader()