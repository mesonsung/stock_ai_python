
'''
程式化交易

    透過自動化程式來下單需要幾項前提：
        1. 證券與期貨開戶
        2. 要申請並簽署「程式交易風險預告暨使用聲明書」及相關文件。
        3. 完成API(Application Program Interface 應用程式介面)串接測試報告回覆給券商。
        4. 多數券商會審核會員資格(也就是每月交易次數達標，或交易額度達標)，才會授權通過。

    如果不會第 3 項，沒關係，找第三方寫好的下單機即可，如：昊瀚資訊 GOrder。
    該產品已經寫好並測試已合作券商的API，方便「訂閱報價」與「委託下單」。
    缺點是使用時必須開啟 GOrder 視窗介面與券商系統進行連線。
    安裝 GOrder 步驟：
        1. 從昊瀚資訊官網(https://www.haohaninfo.com/product_GOrder.php)下載 GOrder.zip
        2. 解壓縮 GOrder.zip 到 GOrder 目錄
        3. 執行 GOrder.exe 進行安裝(下單機程式 + 各券商API)
        4. 執行桌面上的 GOrder 捷徑
        5. 新用戶需註冊昊瀚資訊會員帳號
            5-1. 請務必使用不會阻擋垃圾郵件的電子信箱
            5-2. 收到驗證碼後，輸入確認即可完成註冊
        6. 登入網站會員專區後
            6-1. 點選「透過序號擁有權限」後，輸入試用序號 pyGOrderFun
            6-2. 試用期為 3600 天。
    安裝 Python 套件 haohaninfo 
        pip install haohaninfo
        pip install --upgrade haohaninfo
    透過 GOrder 連接券商系統步驟：
        1. 執行桌面上的 GOrder 捷徑
        2. 昊瀚資訊會員帳密進行登錄
        3. 在右上角選擇要連接的券商
        4. 依連線介面輸入券商開戶的帳密
        5. 保持 GOrder 視窗介面
        6. 執行你的 Python 交易程式
        *. 結束 Python 交易程式後，請關閉 GOrder 視窗介面



程式化交易方式
    日/週/月線交易
        因為頻率慢，價格變動慢(台股盤後幾乎固定)。
        當進出場訊號出現時委託下單成交率高，比較適合新手入門。
        聖杯(指獲利率在80%以上)策略組合複雜度依日/週/月頻率遞減。
        取報價的時間點：
            日線：每天快收盤前。
            週線：每週五快收盤前。
            月線：每月最末日快收盤前。
        取得報價與下單的時間有兩個時間段：
            當日盤中13:20分(台股收盤13:30 | 期貨收盤13:45)
            台股盤後14:00。

    日內當沖交易
        因為頻率快，適合已經有豐富程式交易經驗的老手。
        取報價都是以1分(1M)，然後用程式依頻率轉換成N分線(陰陽燭OHLCV)。
        需要即時分析「五檔報價」與「委買賣量與成交買賣量」。
        聖杯策略組合較複雜。
        進出場訊號反應慢，遠不及價格變動飛快。
        下單成交率低(需要滑價來直接成交)，所以要更精準去停利與停損。

    標的物的手續費與稅金
        當使用 API 交易成功時，回傳資料內會包含手續費與稅金。
        在不考慮國外金融性商品前提下，國內金融性商品因種類區分：
        ！請依證交所與期交所公告為準！
            交易稅：
                股票：0.003，僅在賣出交易時收取。
                期貨：0.00002，每次交易皆收取。
                選擇權：0.001，到期結算 0.00002，每次交易皆收取。
            手續費：
                標準 0.001425，未達20元以20元計，部分會有優惠折扣，每次交易皆收取。




資金控管
    除「期/權」這類商品須儲值保證金方能交易，「低於維持保證金」系統會拒絕委託相對安全。
    台股/ETF商品需要「設定好交割帳戶內的資金」，避免超額交易造成「違約交割」的嚴重問題發生。
    ！！程式化交易的新手最常遇到超額交易造成「違約交割」，雖然券商會有提醒通知，
        重點是龐大的交割金額，還是準備不出來。這就是程式化交易的極高度風險！！



全天候無人監控自動化交易
    若是打造全天候無人的自動化交易，就必須得考量：
    交易程式、交易用主機與網路、電源供應、券商伺服器，其中之一出現問題，就會讓程式化交易無法進行。
        1. 交易程式：最常見就是程式本身的臭蟲、資料異常導致運算錯誤。
        2. 交易用主機與網路：若自行架設需要有備援機制與心跳線機制。
        3. 電源供應：配置UPS不斷電系統，大樓若有電信機房，也需注意可供應時數。
        4. 券商伺服器：大多是連線忙碌導致回應變慢。
    以上 1~4 項，可以部署到雲端主機，但費用很昂貴，也必須有一定網管能力。



交易代理 Trade Agent, TA
    代理使用者進行標的物的交易策略分析與下單交易。
    基本功能如下：
        交易行事曆
            依交易所可交易日期進行新增設定，以允許觸發 TA 的可交易日，或是策略分析時使用。
        資金
            儲值金額設定，以利 TA 下單交易與避免超額交易。
        標的物
            可設定「單個、組合或全部」。
            「組合」部分類似於基金，而「全部」因標的物多則必須搭配「數據中心」做快取分析。
            TA 會依資金量與交易參數進行整股或零股交易。
        對沖避險
            主要在「選擇權」進行反向交易對沖，降低損失。這部分適合大資金的操作。
        策略
            可以將自訂策略(每個策略具有進出場訊號條件與停利損方式)指派給「標的物」進行分析，進而產出交易訊號。
            也是最耗系統運算資源的一塊，必須考量、測試與提升主機硬體等級。
            過度耗用系統運算資源會導致運算時間變得緩慢，喪失程式化交易的美意。
        報價
            日內當沖交易：主要跟券商的報價 API 進行串接訂閱，取得即時報價數據。
            日/週/月線交易：都是以自己建置的「數據中心」進行串接(快取策略條件數據，加快當日收盤分析)。
        交易
            自動化交易下單，主要跟券商的下單 API 或是第三方下單機 API 進行串接。
            分為「多單與空單」交易兩種下單方向。
            若是有設定「對沖避險」則會依策略進行 買進(Call) / 賣出(Put) + 買權(Buy) / 賣權(Sell)。
            交易參數有：整股或零股買賣、All-in、凱利資金配置。
            需要自行管理持有標的物。
        交易紀錄
            將交易結果(無論有無成交或是其他訊息)一律紀錄下來。
            可依類型進行分類紀錄:買賣交易明細、數據串接、策略執行過程、...等。


※以下系統，通常由另一台主機與專屬網路負責，避免 TA 運算效能變差。

交易紀錄代理 Trade Log Agent
    主要從 TA 把交易紀錄複製副本到交易紀錄主機上，以利 RA 與 RS 進行存取。

回報代理 Reply Agent, RA
    將交易結果透過簡訊、即時通訊等回報給使用者知悉。

報表系統 Report System, RS
    依「交易紀錄」擷取相關數據所產出的摘要與明細報表或圖表。
'''




# Python 內建
# 日期時間模組
from datetime import datetime
# 數學模組
import math
# 作業系統模組
import os


# 第三方套件
# 大數據分析模組 1.3.5
import pandas
# 美國 YAHOO 股市模組 0.1.67
import yfinance
# 技術指標模組 0.4.22
import talib
# 圖表模組 3.5.1
import matplotlib.pyplot as plot




# 目前腳本的所在路徑
__path__ = os.path.dirname(__file__)




# 函式::取得個股月線
# 參數
#   <str> symbol 台股證券代碼
# 回傳
def get_stock_month_candles(symbol:str) -> pandas.DataFrame:
    df = pandas.DataFrame()
    # YAHOO台股尾碼 .TW 上市, .TWO 櫃買
    areas = ['TW', 'TWO']
    for area in areas:
        stock = yfinance.Ticker(f'{symbol}.{area}')
        df = stock.history('max', '1mo', actions=False, auto_adjust=True)
        # df.to_csv(f'{__path__}/stock.csv')
        # print(df)
        # exit()
        df.dropna(inplace=True)
        # df.to_csv(f'{__path__}/stock_dropna.csv')
        # exit()
        if df.size > 0:
            # 移除索引
            df.reset_index(inplace=True)
            # 以原始資料(非副本)去除掉有 NaN 的欄位
            df.dropna(inplace=True)
            # 當最後末兩筆都是同月份時，移除最後一筆
            x = df['Date'].apply(lambda v: v.strftime('%Y-%m'))
            if x.iloc[-1] == x.iloc[-2]:
                df.drop(index=df.index[-1], axis=0, inplace=True)
                # df.to_csv(f'{__path__}/stock_drop_last_row.csv')
                # exit()
            break
        else:
            # Adj Close 還原收盤(除權息後的價格)
            df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    return df



'''
長期投資策略
    逢低進場，降低長期持股成本線。
策略條件
    月線 + KD4
    K低於20為1，資金30%
    K低於15為2，資金100%
'''
# 函式::策略-長期投資
# 參數
#   <str> symbol 個股代號
#   <pandas.DataFrame> candles 月線資料
#   <function> event 訊號觸發事件
def strategy_long_term(symbol:str, candles:pandas.DataFrame, event) -> None:
    if type(candles) != pandas.DataFrame: return
    def k_signal(k:float):
        if k >= 20:
            return 0
        if k < 15:
            return 2
        else:
            return 1
    n = 4
    candles['K'], candles['D'] = talib.STOCH(
        candles['High'],
        candles['Low'],
        candles['Close'],
        fastk_period=n,
        slowk_period=n,
    )
    # candles.to_csv(f'{__path__}/stock_kd.csv')
    # exit()
    candles['K'] = candles['K'].fillna(50)
    candles['Signal'] = candles['K'].apply(k_signal)
    # df.to_csv(f'{__path__}/stock_kd_signal.csv')
    # exit()

    if callable(event):
        matches = candles[candles['Signal'] > 0]
        # matches.to_csv(f'{__path__}/stock_kd_signal_matches.csv')
        # exit()
        for index, row in matches.iterrows():
            event(symbol, row['Date'], 'C', row['Close'], row['Signal'])


# 訊號事件
# 參數
#   <str> symbol 證券代碼
#   <datetime> date 交易日期
#   <str> trade 交易單類型: C:多單, B:空單
#   <float> price 進場價格
#   <int> signal 訊號: 訊號值越大，資金投入比例越大
def on_signal(symbol:str, date:datetime, trade:str, price:float, signal:int):
    # 全域::資金與交易紀錄簿
    global fonds, logs
    # 年月
    date = date.strftime('%Y-%m')
    # 收盤價
    price = round(price, 2)
    # 訊號
    if signal == 1:
        # 1 買點: 30%資金
        qty = math.floor(fonds * 0.3 / price)
    else:
        # 2 最佳買點: 100%資金
        qty = math.floor(fonds * 1 / price)

    # 零股數
    b_qty = qty % 1000
    # 零股總額
    b_total = round(price * b_qty)
    # 零股手續費
    b_fee = round(b_total * 0.001425)
    if b_fee < 20: b_fee = 20
    # 零股證交稅
    b_tax = 0
    # 張數(1000股)
    a_qty = math.floor((qty - b_qty) / 1000)
    # 張數總額
    a_total = round(price * a_qty * 1000)
    # 張數手續費
    a_fee = round(a_total * 0.001425)
    if a_fee < 20: a_fee = 20
    # 張數證交稅
    a_tax = 0

    # 正式上線交易，當交易成功時，需要回報的交易紀錄
    #   寫串接 GOrder 或是券商 API 的「委託下單」
    # 轉換成交易紀錄簿資料序列格式
    series = pandas.Series(
        [symbol, date, trade, price, qty, a_total + b_total, a_fee + b_fee, a_tax + b_tax, signal],
        index=logs.columns
    )
    # 寫入交易紀錄簿
    logs = logs.append(series, ignore_index=True)









if __name__ == '__main__':
    # 資金
    fonds = 100000
    # 交易紀錄簿
    logs = pandas.DataFrame(columns=['Symbol', 'Ym', 'Trade', 'Price', 'Qty', 'Total', 'Fee', 'Tax', 'Signal'])

    # 鴻海 2317
    symbol = '2317'
    df = get_stock_month_candles(symbol)
    # 長期投資策略
    strategy_long_term(symbol, df, on_signal)
    # 列舉交易紀錄簿
    for index, log in logs.iterrows():
        date = log['Ym']
        price = log['Price']
        qty = log['Qty']
        total = log['Total']
        fee = log['Fee']
        tax = log['Tax']
        pay = total + fee + tax
        print(f'{date} 價格 {price} 元/股，買進 {qty} 股，總金額 {total} 元，券商手續費 {fee} 元，證券交易稅 {tax} 元，支出 {pay} 元')


    # //// 圖表 /////////////////////////////////////////////////
    # 產生訊號點
    condition = df['Signal'] > 0
    df['Close_Pos'] = df[condition]['Close'].sub(3)
    df['K_Pos'] = df[condition]['K'].sub(3)
    # print(df)
    # 產生索引
    df.index = df['Date']
    # 產生兩個圖表
    fig, ax = plot.subplots(2, 1)
    # 繪製與顯示圖表
    df['Close_Pos'].plot(ax=ax[0], ylabel='Close', xlabel='', color='r', marker='^')
    df['K_Pos'].plot(ax=ax[1], ylabel='K', xlabel='', color='r', marker='^')
    df['Close'].plot(ax=ax[0], ylabel='', xlabel='')
    df['K'].plot(ax=ax[1], ylabel='', xlabel='')
    plot.show()
