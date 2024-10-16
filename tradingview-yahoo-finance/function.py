import yfinance as yf
import pandas as pd
import pandas_ta as ta
import datetime as dt
from datetime import datetime, timedelta
from breeze_connect import BreezeConnect
from supportfunc import expiryofmonth
import time
# Initialize SDK
API_KEY="D9v6t5804@9&M32610~c(025522248^&"
SECRET_KEy="3E83Y6221TP9L*N674313c3E36Ya3W22"
breeze = BreezeConnect(api_key=API_KEY)


def option_data(from_date,to_date,expiry_date,strike_price,option,timeframe,stock_code):
    """from_date=dt.datetime(2024,6,3).isoformat(),to_date=dt.datetime(2024,6,6).isoformat(),expiry_date=dt.datetime(2024,6,5).isoformat(),strike_price=47500"""
    print(from_date,to_date,expiry_date,strike_price,option,timeframe,stock_code,'infunction')
    print('breez1',breeze)
    print(type(from_date),type(to_date),type(expiry_date),type(strike_price),type(option),type(timeframe),type(stock_code))
    data=breeze.get_historical_data_v2(interval=timeframe,
                                from_date= from_date.isoformat(),
                                to_date= to_date.isoformat() ,
                                stock_code=stock_code,
                                exchange_code="NFO",
                                product_type="options",
                                expiry_date=expiry_date.isoformat(),
                                right=option,
                                strike_price=strike_price)
    print(type(strike_price),'typesssss')
    data=pd.DataFrame(data['Success'])
    data=data.rename(columns={'datetime':'timestamp'})
#     data=add_datetime(data)
    
    data.drop(columns= ['exchange_code','product_type','stock_code'],inplace=True)
#     data=vwap(data)
    data['timestamp']=pd.to_datetime(data.timestamp)+ timedelta(hours=6)-timedelta(minutes=30)

    
    data=data.rename(columns={'timestamp':'timestamp','high':'High','close':'Close','low':'Low','open':'Open','open_interest':'oi','strike_price':'STK','volume':'vol','vwap':'vwap'})
    print(data)
    # if(option=='call'):
    #     data=data.rename(columns={'timestamp':'ce_timestamp','high':'ce_high','close':'ce_close','low':'ce_low','open':'ce_open','open_interest':'ce_oi','strike_price':'ce_STK','volume':'ce_vol','vwap':'ce_vwap'})
    # if(option=='put'):
    #     data=data.rename(columns={'timestamp':'pe_timestamp','high':'pe_high','close':'pe_close','low':'pe_low','open':'pe_open','open_interest':'pe_oi','strike_price':'pe_STK','volume':'pe_vol','vwap':'pe_vwap'})
    return  data


def get_authenticate(api_session):
    # Generate Session
    print(api_session,type(api_session))
    breeze.generate_session(api_secret=SECRET_KEy,
                        session_token=api_session['code'])
    print('breez',breeze)
    
def fetch_yahoo_data(from_date,to_date,expiry_date,strike_price,option,timeframe,script_code, ema_period=20, rsi_period=14,interval=5):
    # end_date = datetime.now()
    # if interval in ['1m', '5m']:
    #     start_date = end_date - timedelta(days=7)
    # elif interval in ['15m', '60m']:
    #     start_date = end_date - timedelta(days=60)
    # elif interval == '1d':
    #     start_date = end_date - timedelta(days=365*5)
    # elif interval == '1wk':
    #     start_date = end_date - timedelta(weeks=365*5)
    # elif interval == '1mo':
    #     start_date = end_date - timedelta(days=365*5)

    # data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    
    data =option_data(from_date,to_date,expiry_date,strike_price,option,timeframe,script_code)
    print('mydata',data)
    data['EMA'] = ta.ema(data['Close'], length=ema_period)
    data['RSI'] = ta.rsi(data['Close'], length=rsi_period)

    # candlestick_data = [
    #     {
    #         'time': int(row.Index.timestamp()),
    #         'open': row.Open,
    #         'high': row.High,
    #         'low': row.Low,
    #         'close': row.Close
    #     }
    #     for row in data.itertuples()
    # ]
    candlestick_data = [
        {
            'time': time.mktime(row.timestamp.timetuple()),
            'open': row.Open,
            'high': row.High,
            'low': row.Low,
            'close': row.Close
        }
        for row in data.itertuples()
    ]
    ema_data = [
        {
            'time': time.mktime(row.timestamp.timetuple()),
            'value': row.EMA
        }
        for row in data.itertuples() if not pd.isna(row.EMA)
    ]

    rsi_data = [
        {
            'time': time.mktime(row.timestamp.timetuple()),
            'value': row.RSI if not pd.isna(row.RSI) else 0  # Convert NaN to zero
        }
        for row in data.itertuples()
    ]
    # print(candlestick_data)
    return candlestick_data




