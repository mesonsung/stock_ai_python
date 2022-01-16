# -*- coding: utf-8 -*-
'''
Program    : YAHOO股市交易K線資訊
Author     : 從天慶
Created    : 2021-11-14
Version    : 1.0.0
Description: 提供五分線、日週月線。
             請參考 YAHOO 股市代碼表
'''

# 作業系統模組
import os
# 正規表達式模組
import re
# 大數據分析模組
import pandas
# 美國雅虎股市模組(英文)
import yfinance


# 腳本路徑
__path__ = os.path.dirname(__file__)



# 函式::取得個股K線
# 參數
#   <str> symbol 台股證券代碼
# 回傳
#   <pandas.DataFrame>
def get_stock_candles(symbol:str, **kwargs) -> pandas.DataFrame:
    # 略過股票拆併
    kwargs['actions'] = False
    # 略過除權息還原價格
    kwargs['auto_adjust'] = True
    # 是否使用大盤指數
    if symbol == '': symbol = '^TWII'
    # 產生空的資料表
    df = pandas.DataFrame()
    # 判斷代碼格式
    if re.match(r'^\^[0-9A-Z]+$', symbol):
        # 指數類 ^TWII 台股大盤指數
        stock = yfinance.Ticker(symbol)
        df = stock.history(**kwargs)
    else:
        # 台股類
        # YAHOO台股尾碼 .TW 上市, .TWO 櫃買
        areas = ['TW', 'TWO']
        for area in areas:
            sym = symbol
            if area != '': sym = f'{symbol}.{area}'
            stock = yfinance.Ticker(sym)
            df = stock.history(**kwargs)
            if df.shape[0] > 0:
                break

    # 有資料時
    if df.shape[0] > 0:
        # 移除索引
        df.reset_index(inplace=True)
        # 以原始資料(非副本)去除掉有 NaN 的欄位
        df.dropna(inplace=True)
        # 判斷指定的K線頻率
        if 'interval' in kwargs:
            x = None
            # 週線
            if re.match(r'^[1-9]+wk$', kwargs['interval']):
                # 當最後末兩筆都是同一週時，取得年週
                x = df['Date'].apply(lambda v: v.strftime('%Y-%W'))
            # 月線
            elif re.match(r'^[1-9]+mo$', kwargs['interval']):
                # 當最後末兩筆都是同月份時，取得年月
                x = df['Date'].apply(lambda v: v.strftime('%Y-%m'))
            # 是週月線的話，更新高低收量後，移除最後一筆
            if type(x) == pandas.Series:
                prev = df.iloc[-2]
                last = df.iloc[-1]
                if x.iloc[-1] == x.iloc[-2]:
                    # 前一筆更新
                    prev_i = df.tail(1).index[0] - 1
                    df.at[prev_i, 'High'] = max(prev['High'], last['High'])
                    df.at[prev_i, 'Low'] = min(prev['High'], last['High'])
                    df.at[prev_i, 'Close'] = last['Close']
                    df.at[prev_i, 'Volume'] += last['Volume']
                    # 移除末筆(最新的交易日)
                    df.drop(index=df.index[-1], axis=0, inplace=True)
        # 處理小數位數
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = round(df[col], 2)
        df['Volume'] = round(df['Volume'])
    else:
        # 空資料表時，補上欄位名稱
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    # 將分線的 Datetime 欄位名稱改為 Date
    if re.match(r'^[1-9]+m$', kwargs['interval']):
        df.rename(columns={'Datetime':'Date'}, inplace=True)
    # 設定索引為日期
    df.index = df['Date']
    return df



# 函式::取得個股5分線
# 參數
#   <str> symbol 台股證券代碼
# 回傳
#   <pandas.DataFrame>
def get_stock_5m_candles(symbol:str, **kwargs):
    if 'interval' in kwargs: del kwargs['interval']
    if 'period' in kwargs: del kwargs['period']
    return get_stock_candles(symbol, interval='5m', period='5d')


# 函式::取得個股日線
# 參數
#   <str> symbol 台股證券代碼
# 回傳
#   <pandas.DataFrame>
def get_stock_daily_candles(symbol:str, **kwargs):
    if 'interval' in kwargs: del kwargs['interval']
    return get_stock_candles(symbol, interval='1d', **kwargs)


# 函式::取得個股週線
# 參數
#   <str> symbol 台股證券代碼
# 回傳
#   <pandas.DataFrame>
def get_stock_week_candles(symbol:str, **kwargs):
    if 'interval' in kwargs: del kwargs['interval']
    return get_stock_candles(symbol, interval='1wk', **kwargs)


# 函式::取得個股月線
# 參數
#   <str> symbol 台股證券代碼
# 回傳
#   <pandas.DataFrame>
def get_stock_month_candles(symbol:str, **kwargs):
    if 'interval' in kwargs: del kwargs['interval']
    return get_stock_candles(symbol, interval='1mo', **kwargs)




# 模組測試
if __name__ == '__main__':
    symbol= '2317'

    print(f'{symbol} - 5分線資料')
    df = get_stock_5m_candles(symbol)
    print(df)
    os.system('pause')

    print(f'{symbol} - 日線資料')
    df = get_stock_daily_candles(symbol, start='2021-01-01')
    print(df)
    os.system('pause')

    print(f'{symbol} - 週線資料')
    df = get_stock_week_candles(symbol, start='2021-12-01')
    print(df)
    os.system('pause')

    print(f'{symbol} - 月線資料')
    df = get_stock_month_candles(symbol, period='max')
    print(df)
    os.system('pause')

    print('大盤日線資料')
    df = get_stock_daily_candles('')
    print(df)
    os.system('pause')