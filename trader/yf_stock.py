


'''
yfinance 0.1.67
    https://pypi.org/project/yfinance/
    Released: Nov 21, 2021
    pip install yfinance==0.1.67
    pip install --upgrade yfinance==0.1.67

matplotlib 3.5.1
    https://pypi.org/project/matplotlib/
    Released: Dec 11, 2021
    pip install matplotlib==3.5.1
    pip install --upgrade matplotlib==3.5.1
    import matplotlib.pyplot as plt

mplfinance 0.12.8b4
    https://pypi.org/project/mplfinance/
    Released: Dec 14, 2021
    pip install mplfinance==0.12.8b4
    pip install --upgrade mplfinance==0.12.8b4
'''


# 美國YAHOO股市數據模組
import yfinance as yf
# 財務圖表模組
import mplfinance as mpf


'''
Ticker 類別
    產生股票爬蟲物件
    建構式參數
        ticker: 股票代碼
                台灣個股尾碼需加.TW，例如:台積電 2330.TW
                大盤加權指數代碼 ^TWII
        session: 工作階段參數，預設 None
'''
stock_no = '2371.TW'
stock = yf.Ticker(stock_no)


'''
info 屬性
    取得個股的基本資訊(英文)
    例如公司名、行業、市值、以及一系列的財務比率(Financial Ratios) 如 P/E, P/B 比率等。
'''
print(stock.info)


'''
financials 屬性
    公司的損益表(Income Statement)
    一次可以獲取 4 年的數據。
'''
print(stock.financials)


'''
earnings 屬性
    公司 4 年間的總收入(Revenue)與盈虧(Earnings)，即 Top-line 與 Bottom-line 數據
'''
print(stock.earnings)


'''
actions 屬性
    公司的企業行動(Corporate Action)資料，例如股息(Dividend)和拆股(Stock Split)
    股票拆分: 概念跟換錢一樣，將大鈔兌換成零錢，將零錢湊整兌換大鈔，分為「分割與反分割」。
        拆分: 將1股50元，拆成10股各5元，其總價值沒變，股數增加，但每股價值變小。
                特色: 股數增加，讓股票大量流通。
                目的: 公司看好未來 (為了壓低股價，以讓更多人能購買股票，所以這可視為公司看好未來發展)
        合併: 將10股各5元，合併成1股50元，其總價值沒變，股數減少，但每股價值變大。
                特色: 讓股價更好看，吸引大資金進駐。
                目的: 公司保守看待未來 (股票合併通常不是什麼好事，通常代表公司預期未來較保守，才會用反分割來“人為”調高股價)
'''
print(stock.actions)


'''
history() 方法參數
    period 週期: 要下載的數據週期，預設 1mo
        有效參數值: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    interval 頻率: K線頻率(分線的週期限5日)，預設 1d
        有效參數值: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    start 起始日期: 若不使用 period 參數時，就必須設定
        日期格式: YYYY-MM-DD
    end 結束日期: 若不使用 period 參數時，就必須設定
        日期格式: YYYY-MM-DD
    prepost 是否包含前後市場數據: 預設 False
    auto_adjust 是否自動調整OHLC: 預設 True
    actions 是否取得股票利息(dividends)與股票拆分事件(splits events)


'''
df_history = stock.history(period='1y', interval='1d', auto_adjust=False)
print(df_history)


'''
download() 靜態方法
    一次可下載多檔個股。
    參數
        group_by 設定個股群組欄位名稱。
        threads 設為 True 則可以用多執行緒下載，預設 False。
        ...其餘同 Ticker 類別建構參數
    回傳 DataFrame

    若要指定某個個股群組，使用 DataFrame['個股代碼']
        stocks['2330.TW']
'''
stocks = yf.download(
    '2317.TW 2371.TW',
    group_by='ticker',
    period='5d',
    auto_adjust=True
)
print(stocks)
print(stocks['2317.TW'])
print(stocks['2371.TW'])


'''
繪製財務圖表
'''
mpf.plot(
    df_history,
    type='candle',
    volume=True,
    title=stock_no,
    datetime_format='%Y-%m-%d'
)