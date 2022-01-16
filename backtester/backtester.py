
'''
backtrader
    標準數據集合 lines
        在「回測用數據(Data Feeds), 指標(Indicators) 及策略(Strategis)」裡都有此集合之屬性 lines。
        一個標準數據(Line)包含：時間 datetime, 開 open, 高 high, 低 low, 收 close, 量 volume, 未平倉量 openinterest
        經由日期序列化後即產生了標準數據集合(lines)。
    數據索引 index
        所有的數據在存取時，都是使用指標(Cursor)。
             0: 目前索引指向的位置
            -1: 指向前一筆的位置


    核心架構
        回測數據源 (Data Feed)：
        
        交易策略 (Strategy)：
            策略演算函式必須回傳出買/賣訊號
        
        回測環境設置 (Cerebro)：
            初始資金、佣金、回測用數據、交易策略、每筆交易投入金額

        執行回測 (Run)

        回測分析 (Analyzers)
'''
import math
import os
import re
# 
import yahoostock
# 
import pandas
import numpy as np
import talib
# 交易回測模組
import backtrader as bt


__path__ = os.path.dirname(__file__)
os.makedirs(f'{__path__}/temp', 0o755, True)





# 自訂策略類別(繼承 backtrader.Strategy)
class LongTerm(bt.Strategy):
    __symbol = ''
    __dataframe = None
    __temp_path = ''
    __log_file = ''
    __strategy_file = ''
    __orders = None

    def __init__(self, symbol:str, df:pandas.DataFrame):
        self.__symbol = symbol
        self.__dataframe = df
        # KD 隨機震盪指標 5-3-3
        self.k, self.d = talib.STOCH(
            df['High'],
            df['Low'],
            df['Close'],
            fastk_period=5,
            slowk_period=3,
            slowk_matype=0,
            slowd_period=3,
            slowd_matype=0
        )
        # 濾出買賣訊號
        self.signals = self.k.apply(lambda k: self.__signal(k))
        df['K'] = self.k
        df['D'] = self.d
        df['Signal'] = self.signals
        # 建立暫存目錄
        self.__create_temp_folder()
        # 輸出分析紀錄
        df.to_csv(self.__strategy_file)

    def __create_temp_folder(self):
        self.__temp_path = __path__ + '/temp'
        os.makedirs(self.__temp_path, exist_ok=True)
        self.__strategy_file = f'{self.__temp_path}/{__class__.__name__}_{self.__symbol}.csv'
        self.__log_file = f'{self.__temp_path}/log_{self.__symbol}.txt'

    def __signal(self, k:float) -> int:
        if math.isnan(k): return 0
        if k >= 15:
            if k > 95:
                return -2
            elif k > 88:
                return -1
            else:
                0
        if k < 10:
            return 2
        elif k < 15:
            return 1

    @staticmethod
    def write_log(filename:str, message:str):
        with open(filename, 'a', encoding='utf-8') as wr:
            wr.write(f'{message}\n')

    def __log(self, message:str):
        print(message)
        LongTerm.write_log(self.__log_file, message)


    # 覆寫實做 next() 方法
    def next(self):
        if self.__orders: return
        # 目前日期
        curr_date = self.datas[0].datetime.date(0)
        # 目前收盤價
        curr_close = self.datas[0].close[0]
        # 持倉狀態
        pos = self.position
        # 取目前索引
        index = len(self) - 1
        # 目前訊號
        curr_signal = self.signals[index]
        if np.isnan(curr_signal): return 
        self.broker.add_cash(10000)
        if curr_signal > 0:
            cash = self.broker.get_cash()
            if curr_signal == 1: cash *= 0.3
            qty = math.floor(cash / curr_close / 1000)
            qty = math.floor(qty * 1000)
            self.__orders = self.buy(size=qty)
            self.__log(f'買進 >> 月線 {curr_date}, 收盤價 {curr_close:.2f}, 數量:{qty}, 訊號 {curr_signal}')
        if pos:
            # 有部位，可以賣出
            if curr_signal < 0:
                cash = self.broker.get_value()
                qty = pos.size
                qty *= 0.3
                self.__orders = self.sell(size=qty)
                self.__log(f'賣出 >> 月線 {curr_date}, 收盤價 {curr_close:.2f}, 數量:{qty}, 訊號 {curr_signal}')

    # 覆寫實做 notify_trade() 交易通知方法
    def notify_trade(self, trade):
        if not trade.isclosed: return
        self.__log("交易收益：毛利 %.2f 淨利：%.2f" % (trade.pnl, trade.pnlcomm))

    # 覆寫實做 notify_order() 下單方法
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.__log("買入 價格: %.2f 成本: %.2f 手續費: %.2f" % (order.executed.price, order.executed.value, order.executed.comm))
            elif order.issell():
                self.__log("賣出 價格: %.2f 成本: %.2f 手續費: %.2f" % (order.executed.price, order.executed.value, order.executed.comm))
                
            self.bar_executed = len(self)
                
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.__log("訂單取消/餘額不足/拒絕交易")

        self.__orders = None




def backtest(symbol:str, df:pandas.DataFrame):
    # 產生經紀人
    bk = bt.BackBroker()
    # 設定初始資金
    bk.set_cash(100000)
    # 設定手續費
    bk.setcommission(commission = 0.001425)


    # 產生回測器
    cb = bt.Cerebro()
    # 加入數據源
    cb.adddata(bt.feeds.PandasData(dataname=df))
    # 設定經紀人
    cb.broker = bk
    # 加入自訂策略
    cb.addstrategy(LongTerm, symbol, df)
    # 執行回測
    log_file = f'{__path__}/temp/log_{symbol}.txt'
    LongTerm.write_log(log_file, f'起始資金NT$ {bk.get_value():,.0f}')
    cb.run()
    LongTerm.write_log(log_file, f'最後資金NT$ {bk.get_value():,.0f}\n\n\n\n')
    # 繪製圖表與儲存圖表
    image_file = f'{__path__}/temp/chart_{symbol}.png'
    figure = cb.plot()[0][0]
    figure.savefig(image_file)


def ui():
    while True:
        # 清除畫面
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        # 等候用戶輸入資料
        symbol = input('請輸入證券代碼 [Q]:離開]: ')
        # 當輸入 Q 離開本程式
        if (symbol.lower() == 'q'): exit()
        # 驗證代碼，不正確就重頭來
        if not re.match(r'^[0-9]{4}$', symbol):
            print('\n代碼錯誤，請重新輸入')
            input('...請按 ENTER 鍵繼續')
            continue
        # 代碼驗證通過
        # 取得回測用數據
        df = yahoostock.get_stock_month_candles(symbol, period='max')
        # df = yahoostock.get_stock_week_candles(symbol, period='max')
        # df = yahoostock.get_stock_daily_candles(symbol, period='max')
        if df.size < 1:
            print(f'證券代碼:{symbol} 沒有數據，無法回測')
            input('...請按 ENTER 鍵繼續')
        else:
            # 回測
            backtest(symbol, df)



if __name__ == '__main__':
    ui()