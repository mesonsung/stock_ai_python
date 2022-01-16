
'''
技術指標 Indicator

    所謂的「指標」是基於量化數據、統計演算所產生。
    再依照「指標的運用規則」與「回測分析」來過濾出所謂的「訊號(Signal)」。

    以投資市場來說
        量化數據：價格(開高低收)與成交量(總成交量與內外盤成交量)。
        統計演算：基於一個理論基礎所設計的演算規則，投入價格或成交量，亦或者是兩者都需要。
                    最後產生出的分析數據。
        回測分析：將分析數據，進行歷史軌跡回測來判讀訊號與驗證其準確率。

    指標種類
        疊加指標 Overlays：
            特徵是統計演算後的分析數據，在圖表上可以疊加在價格與成交量上面直接研判區間走勢。
            例如：簡單移動平均(SMA)、布林通道(BBands)、逆勢操作系統(CDP)、能量潮(OBV)。
        震盪指標 Oscillators：
            特徵是統計演算後的分析數據是種震盪比較率，透過另一個副圖表來對照價格與成交量。
            例如：隨機震盪(KD)、相對強弱(RSI)、指數平滑移動平均(MACD)、平均震幅(ATR)。

    移動與扣抵
        大多數的統計演算都是取Ｎ個交易日(包含當日)的量化數據來進行移動演算。
        1   2   3   4   5   6   7   8   9   10   ... >>>
        |<----- N ------|
        
        也因為移動演算的特性，範圍框會向前移動，自然就會汰除區間內第一個交易日，稱之「扣抵」日。
        1   2   3   4   5   6   7   8   9   10   ... >>>
        扣----- N ------|
            扣----- N ------|
                扣----- N ------|
        
        藉由比較「當日與扣抵日」的價格差，來推算次日價格。
        5   8   9  10   7   3   4   5   7   9    ... >>>
        扣----- N ------|      當日價格 7 > 扣抵日價格 5 ，因為扣抵比當日價格低，稱之「扣低」。
            扣----- N ------|  當日價格 3 < 扣抵日價格 8 ，因為扣抵比當日價格高，稱之「扣高」。
        ※「扣低」通常代表價格走高，「扣高」通常代表價格走低。

    指標漏洞與背離
        在資安界常言道，每種技術都潛藏著漏洞，只差別你不知駭客知。
            簡單平均法：求所有值總和的平均，但它的漏洞就是離群值。
            也就是在出現極高極低值的情況下，均價就會瞬間拉高拉低。
        主力會利用此移動演算特性，以及震盪指標函式的價量參數，進行特意拉高或拉低價格，
        使之「指標背離」原有的常態移動率，進而讓指標失準或背離，讓市場投資者誤導走勢。

    指標參數
        參數的調校會影響演算結果，其結果會有三種狀態：
            過適(擬合過度 Overfitting)：敏感度太高，雜訊增加。
            最適(擬合最佳化 Optimization)：剛剛好。
            乏適(擬合不足 Underfitting)：敏感度太低，訊號減少。
        主力控盤會有自己的參數，來控制個股的價格。
        坊間所謂的神奇參數，也是針對某幾檔個股主力慣用的參數。

指標永遠是落後
    指標永遠是將現有的數據進行演算，並透過圖面分析與回測，才能推測可能的走勢。
    指標的運用也遵循其演算規則與統計機率來執行進出場。

'''


'''
Pandas 大數據分析模組

    DataFrame 資料框架，類似於資料表。
        是由多個 Series 序列所組成，可以是資料列或資料欄。

    axis 滾動軸方向
        0: Row 資料列(行)
        1: Column 資料欄(列)

            1   2   3   4   5  Column
            ---------------->
        1   |
        2   |
        3   |
        4   |
        5   ↓
        Row

    diff(periods=1) 計算目前位置與前幾個位置之間內容值的差值

    shift(periods=1) 取前幾個

    rolling(window=5) 滾動視窗
    1   2   3   4   5   6   7   8   9   10
    |<----- 5 ------|
        |<----- 5 ------|
            |<----- 5 ------|

    expanding(min_period=1) 擴張
    1   2   3   4   5   6   7   8   9   10
    |-->|
    |------>|
    |---------->|

    iloc[row_index, column_index] 依索引位置取值，但無法賦值

    iat[row_index, column_index] = value 依索引位置取值與賦值

'''






# 作業系統
import os
# 從型態模組匯入可列舉類別
from typing import Iterable

# 大數據分析模組
import pandas
# 多維陣列運算模組
import numpy



# 暫存目錄 ./temp
__path__ = os.path.dirname(__file__)
temp_path = f'{__path__}/temp'
os.makedirs(temp_path, 0o755, exist_ok=True)



# 空序列
def empty_series():
    return pandas.Series(dtype=numpy.float64)



'''
Simple Moving Average (SMA)
簡單移動平均

SMA = N日內的價格總和 / N
'''
# 函式::簡單移動平均
# 參數
#   <pandas.Series> closes 收盤價
#   <int> n 週期(5)
# 回傳
#   <pandas.Series>
def SMA(closes:pandas.Series, n:int=5) -> pandas.Series:
    if closes.shape[0] < 1: return empty_series()
    sma = closes.rolling(n).mean()
    return round(sma, 2)


'''
Exponential Moving Averages (EMA)
指數移動平均
'''
# 函式::指數移動平均
# 參數
#   <pandas.Series> closes 收盤價
#   <int> n 週期(5)
# 回傳
#   <pandas.Series>
def EMA(closes:pandas.Series, n:int=5) -> pandas.Series:
    if closes.shape[0] < 1: return empty_series()
    alpha = 2 / (n + 1)
    ema = closes.ewm(alpha=alpha, min_periods=n, adjust=False).mean()
    return round(ema, 2)


'''
Weighted Moving Average (WMA)
加權移動平均
'''
# 函式::加權移動平均
# 參數
#   <pandas.Series> closes 收盤價
#   <int> n 週期(5)
# 回傳
#   <pandas.Series>
def WMA(closes:pandas.Series, n:int=5) -> pandas.Series:
    if closes.shape[0] < 1: return empty_series()
    weight = numpy.arange(1, n + 1)
    wma = closes.rolling(n).apply(lambda c: numpy.dot(c, weight) / weight.sum(), raw=True)
    return round(wma, 2)


'''
Cumulative Moving Averages (CMA)
累積移動平均
'''
# 函式::累積移動平均
# 參數
#   <pandas.Series> closes 收盤價
# 回傳
#   <pandas.Series>
def CMA(closes:pandas.Series) -> pandas.Series:
    if closes.shape[0] < 1: return empty_series()
    cma = closes.expanding(1).mean()
    return round(cma, 2)



'''
多空分界指標
    由四個簡單平均值再進行平滑處理
'''
def CBI(closes:pandas.Series, n1:int=6, n2:int=12, n3:int=26, n4:int=72) -> pandas.Series:
    if closes.shape[0] < 1: return empty_series()
    sma1 = closes.rolling(n1).mean()
    sma2 = closes.rolling(n2).mean()
    sma3 = closes.rolling(n3).mean()
    sma4 = closes.rolling(n4).mean()
    cbi = (sma1 + sma2 + sma3 + sma4) / 4
    return round(cbi, 2)




'''
BIAS
乖離率/平均報酬率
    價格與均線的偏離率。
    當價格異常拉高或拉低時，乖離就瞬間拉大
    當乖離在 +/-0.03 都算是常態波動
'''
def BIAS(closes:pandas.Series, n:int=5) -> pandas.Series:
    if closes.shape[0] < 1: return empty_series()
    sma = round(closes.rolling(n).mean(), 2)
    bias = round((closes - sma) / sma, 2)
    return bias




'''
Moving Average Convergence Divergence
指數移動平均收斂或分歧
    由兩條快慢週期的指數均值所產生的交叉指標
    當快線跨越慢線且兩線都上彎，稱之黃金交叉
    當慢線穿越快線且兩線都下彎，稱之死亡交叉
    以零軸區分多空，在 +/-2 區間內屬常態波動
    若超過 +/-2 屬於多空頭趨勢過熱，當出現交叉時也代表趨勢將出現大反轉，典型V形反轉
    這也是投顧法人常用指標，又稱為致富法人線
'''
# 函式::指數移動平均收斂與分歧
# 參數
#   <pandas.Series> closes 收盤價
#   <int> fast 快線週期(12)
#   <int> slow 慢線週期(26)
#   <int> n 快慢線差離週期(9)
# 回傳
#   <pandas.Series>: dif, dem, osc
def MACD(closes:pandas.Series, fast:int=12, slow:int=24, n:int=9) -> Iterable:
    if closes.shape[0] < 1: return empty_series(), empty_series(), empty_series()
    fast = EMA(closes, fast)
    slow = EMA(closes, slow)
    dif = fast - slow
    dem = EMA(dif, n)
    osc = dif - dem
    return round(dif, 2), round(dem, 2), round(osc, 2)





'''
RSI
相對強弱
    也是投顧法人常用指標之一，利用週期內的漲跌幅率來進行指數平滑。
    可以反映週期內走勢強弱，50 為多空分界，低於 20 屬於賣超，高於 80 屬於買超。
    有的會使用雙週期(6,12)，來進行短線操作。
    也是因為反應準確，所以主力會利用移動扣抵特性刻意再拉高與拉低產生背離混淆視聽。
'''
# 函式::相對強弱
# 參數
#   <pandas.Series> closes 收盤價
#   <int> n 週期(6)
# 回傳
#   <pandas.Series>
def RSI(closes:pandas.Series, n:int=6) -> pandas.Series:
    if closes.shape[0] < 1: return empty_series()
    df = pandas.DataFrame(closes)
    df.columns = ['close']
    df['dif'] = df['close'].diff(1)
    df['up'] = df['dif'].apply(lambda dif: dif if dif > 0 else 0)
    df['dn'] = df['dif'].apply(lambda dif: abs(dif) if dif < 0 else 0)
    df['ema-up'] = df['up'].ewm(span=n, min_periods=n).mean()
    df['ema-dn'] = df['dn'].ewm(span=n, min_periods=n).mean()
    df['rs'] = df['ema-up'].div(df['ema-dn'])
    df['rsi'] = round(df['rs'].apply(lambda rs: rs / (1 + rs) * 100), 2)
    df.to_csv(f'{temp_path}/rsi.csv')
    return df['rsi']



'''
MTM
動量指標
    運用期間內的差離扣抵反應價格走勢，以零軸為多空分界
    缺點是轉折太多，會搭配MTM均線，進行短線波段操作
'''
# 函式::動量指標
# 參數
#   <pandas.Series> closes 收盤價
#   <int> n 週期(20)
# 回傳
#   <pandas.Series>: mtm, mtm-sma
def MTM(closes:pandas.Series, n:int=12) -> Iterable:
    if closes.shape[0] < 1: return empty_series(), empty_series()
    mtm = round(closes.diff(n), 2)
    sma_mtm = round(mtm.rolling(n).mean(), 2)
    df = pandas.DataFrame(index=closes.index,
        data={
            'close': closes,
            'mtm': mtm,
            'sma_mtm': sma_mtm
        }
    )
    df.to_csv(f'{temp_path}/mtm.csv')
    return mtm, sma_mtm


'''
CMO
錢德動量震盪指標
    演算原理類似於RSI
    差別是RSI是反應週期內的漲幅率，而CMO是反應週期內的高低差振幅率
'''
# 函式::錢德動量震盪指標
# 參數
#   <pandas.Series> closes 收盤價
#   <int> n 週期(26)
# 回傳
#   <pandas.Series>: 
def CMO(closes:pandas.Series, n:int=26) -> pandas.Series:
    if closes.shape[0] < 1: return empty_series()
    df = pandas.DataFrame(closes)
    df.columns = ['close']
    df['dif'] = round(df['close'].diff(1), 2)
    df['up'] = df['dif'].apply(lambda dif: dif if dif > 0 else 0)
    df['dn'] = df['dif'].apply(lambda dif: abs(dif) if dif < 0 else 0)
    df['up'] = round(df['up'].rolling(n).sum(), 2)
    df['dn'] = round(df['dn'].rolling(n).sum(), 2)
    df['cmo'] = round((df['up'] - df['dn']) / (df['up'] + df['dn']) * 100, 2)
    df.to_csv(f'{temp_path}/cmo.csv')
    return df['cmo']

'''
KDJ
隨機震盪
'''
# 函式::隨機震盪
# 參數
#   <pandas.Series> highs 最高價
#   <pandas.Series> lows 最低價
#   <pandas.Series> closes 收盤價
#   <int> n 週期(9)
# 回傳
#   <pandas.Series>: rsv, k, d, j, j2
def KDJ(highs:pandas.Series, lows:pandas.Series, closes:pandas.Series, n:int=9) -> Iterable:
    if closes.shape[0] < 1: return empty_series(), empty_series(), empty_series(), empty_series(), empty_series()
    df = pandas.DataFrame()
    df['high'] = highs
    df['low'] = lows
    df['close'] = closes
    df['min'] = lows.rolling(n).min()
    df['max'] = highs.rolling(n).max()
    df['rsv'] = round((df['close'] - df['min']) / (df['max'] - df['min']) * 100, 2)
    df['rsv'] = df['rsv'].fillna(50)
    df['k'] = 50
    df['d'] = 50
    for index, rsv in df['rsv'].iteritems():
        if index < n - 1: continue
        k_prev = df['k'].iloc[index - 1]
        k = round(2/3 * k_prev + 1/3 * rsv, 2)
        df['k'].at[index] = k
        d_prev = df['d'].iloc[index - 1]
        d = round(2/3 * d_prev + 1/3 * k, 2)
        df['d'].at[index] = d
    df['j'] = round(3 * df['d'] - 2 * df['k'], 2)
    df['j2'] = round(3 * df['k'] - 2 * df['d'], 2)
    df.to_csv(f'{temp_path}/kdj.csv')
    return df['rsv'], df['k'], df['d'], df['j'], df['j2']


'''
Average True Range (ATR)
平均真實振幅
    評估週期內的波動，最常用於移動停利損，或是區間來回套利
'''
# 函式::平均真實振幅
# 參數
#   <pandas.Series> highs 最高價
#   <pandas.Series> lows 最低價
#   <pandas.Series> closes 收盤價
#   <int> n 週期(6)
# 回傳
#   <pandas.Series>
def ATR(highs:pandas.Series, lows:pandas.Series, closes:pandas.Series, n:int=14) -> pandas.Series:
    if closes.shape[0] < 1: return empty_series()
    high_low = highs - lows
    high_close = abs(highs - closes.shift())
    low_close = abs(lows - closes.shift())
    ranges = pandas.concat([high_low, high_close, low_close], axis=1)
    tr = numpy.max(ranges, axis=1)
    atr = tr.rolling(n).mean()
    for i in range(n, atr.size):
        atr.at[i] = round((atr.iloc[i - 1] * (n - 1) + tr.iloc[i]) / n, 2)
    df = pandas.DataFrame(index=closes.index,
        data={
            'close': round(closes, 2),
            'high-low': round(high_low, 2),
            'high-close': round(high_close, 2),
            'low-close': round(low_close, 2),
            'tr': round(tr, 2),
            'atr': round(atr, 2)
        }
    )
    df.to_csv(f'{temp_path}/atr.csv')
    return df['atr']




'''
On-Balance Volume (OBV)
能量潮
    量比價先行，以收盤漲跌加減累計成交量。
'''
# 函式::能量潮
# 參數
#   <pandas.Series> closes 收盤價
#   <pandas.Series> volumes 成交量
#   <int> n SMA週期(20)
# 回傳
#   <pandas.Series>: obv, obv-ma
def OBV(closes:pandas.Series, volumes:pandas.Series, ma:int=20) -> Iterable:
    if closes.shape[0] < 1: return empty_series(), empty_series()
    def up_dn(c:float):
        if c > 0: return 1
        if c == 0: return 0
        if c < 0: return -1
    dif = closes.diff(1)
    dif = dif.apply(up_dn)
    df = pandas.concat([closes, volumes, dif], axis=1)
    df.columns = ['close', 'volume', 'dif']
    df['obv'] = df['volume'] / 2
    for index, row in df.iterrows():
        if index == 0:
            continue
        if row['dif'] > 0:
            row['obv'] = df.iloc[index - 1]['obv'] + row['volume']
        elif row['dif'] < 0:
            row['obv'] = df.iloc[index - 1]['obv'] - row['volume']
        else:
            row['obv'] = df.iloc[index - 1]['obv']
    df['obv'] = round(df['obv'])
    df['obv-ma'] = round(df['obv'].rolling(ma).mean())
    df.to_csv(f'{temp_path}/obv.csv')
    return df['obv'], df['obv-ma']



'''
(BBands)
布林通道
'''
def BBands(closes:pandas.Series, n:int=20) -> Iterable:
    if closes.shape[0] < 1: return empty_series(), empty_series(), empty_series()
    sma = closes.rolling(n).mean()
    std = closes.rolling(n).std()
    up = sma + 2 * std
    dn = sma - 2 * std
    df = pandas.DataFrame(index=closes.index,
        data={
            'close': closes,
            'sma': round(sma, 2),
            'std': round(std, 2),
            'up': round(up, 2),
            'dn': round(dn, 2)
        }
    )
    df.to_csv(f'{temp_path}/bbands.csv')
    return df['up'], df['sma'], df['dn']



'''
CDP
逆勢操作
    1. 以前一日的高低收求今日的 CDP
        CDP = (前日高 + 前日低 + 前日收 * 2) / 4
    2. 求出今日極限 A 的高 H 低 L
        AH = CDP + (前日高 - 前日低)
        AL = CDP - (前日高 - 前日低)
    3. 求出今日相對 N 的高 H 低 L
        NH = CDP * 2 - 前日低
        NL = CDP * 2 - 前日高
'''
def CDP(highs:pandas.Series, lows:pandas.Series, closes:pandas.Series) -> Iterable:
    if closes.shape[0] < 1: return empty_series(), empty_series(), empty_series(), empty_series(), empty_series()
    cdp = (highs.shift() + lows.shift() + closes.shift() * 2) / 4
    ah = cdp + (highs.shift() - lows.shift())
    nh = cdp * 2 - lows.shift()
    nl = cdp * 2 - highs.shift()
    al = cdp - (highs.shift() - lows.shift())
    df = pandas.DataFrame(index=closes.index,
        data={
            'high': highs,
            'low': lows,
            'closes': closes,
            'cdp': round(cdp, 2),
            'ah': round(ah, 2),
            'nh': round(nh, 2),
            'nl': round(nl, 2),
            'al': round(al, 2)
        }
    )
    # 
    data = []
    data.insert(0, {'ah':None, 'nh':None, 'cdp':None, 'nl':None, 'al':None})
    pandas.concat([pandas.DataFrame(data), df], ignore_index=True)
    # 
    df.to_csv(f'{temp_path}/cdp.csv')
    return df['ah'], df['nh'], df['cdp'], df['nl'], df['al']



'''
Lohas
樂活五線譜

藉由五條線來判斷走勢與買賣區間
原理
    利用月線周期3.5年(42個月)劃出一條趨勢線，也是多空分界線
    計算出該期間的標準差
    樂觀線：    以趨勢線 + 2個標準差    => 上漲機率 2.5%，下跌機率 97.5%
    相對樂觀線：以趨勢線 + 1個標準差    => 上漲機率 16%，下跌機率 84%
    相對悲觀線：以趨勢線 - 1個標準差    => 下跌機率 16%，上漲機率 84%
    悲觀線：    以趨勢線 - 2個標準差    => 下跌機率 2.5%，上漲機率 97.5%
    由四條線區隔出六個區間帶，由下到上分別為 1 ~ 6
    3 ~ 4 區間帶為正常區間
'''
def LOHAS(closes:pandas.Series) -> Iterable:
    if closes.shape[0] < 1: return empty_series(), empty_series(), empty_series(), empty_series(), empty_series()
    # 運用線性回歸產生趨勢線
    from scipy.stats import linregress
    regression = linregress(x=closes.index, y=closes)
    trend = numpy.round(regression[1] + regression[0] * closes.index, 2)
    # 計算標準差
    std = numpy.round(closes.std(axis=0), 2)
    # 產生四條線
    df = pandas.DataFrame(index=closes.index, data={'close':closes, 'trend':trend})
    df['trend-ah'] = numpy.round(trend + 2 * std, 2)
    df['trend-nh'] = numpy.round(trend + std, 2)
    df['trend-nl'] = numpy.round(trend - std, 2)
    df['trend-al'] = numpy.round(trend - 2 * std, 2)
    df.to_csv(f'{temp_path}/trend.csv')
    return df['trend-ah'], df['trend-nh'], df['trend'], df['trend-nl'], df['trend-al']

def LOHAS2(closes:pandas.Series, n:int=42) -> Iterable:
    if closes.shape[0] < 1: return empty_series(), empty_series(), empty_series(), empty_series(), empty_series()
    df = pandas.DataFrame(index=closes.index, data={'close':closes})
    df['trend-ah'] = 0
    df['trend-nh'] = 0
    df['trend'] = 0
    df['trend-nl'] = 0
    df['trend-al'] = 0
    from scipy.stats import linregress
    index = 0
    while index < closes.size:
        si = index
        ei = index + n
        if ei > closes.size: ei = closes.size
        #
        ranges = closes[si : ei]
        regression = linregress(x=ranges.index, y=ranges)
        trends = numpy.round(regression[1] + regression[0] * ranges.index, 2)
        std = round(ranges.std(axis=0), 2)
        #
        for i in range(0, ranges.size):
            t = trends[i]
            j = i + index
            df['trend'].at[j] = t
            df['trend-ah'].at[j] = round(t + 2 * std, 2)
            df['trend-nh'].at[j] = round(t + std, 2)
            df['trend-nl'].at[j] = round(t - std, 2)
            df['trend-al'].at[j] = round(t - 2 * std, 2)
        index += n
    df.to_csv(f'{temp_path}/trend.csv')
    return df['trend-ah'], df['trend-nh'], df['trend'], df['trend-nl'], df['trend-al']


'''
Lohas
樂活通道

藉由三條線來判斷走勢與買賣區間
原理
    利用週均線周期20周(100日)劃出一條趨勢線，也是多空分界線。
    計算出周期內最高與最低的振幅率K。
    上軌：周期內最高 * (1 + 2個振幅率)。
    下軌：周期內最低 * (1 - 2個振幅率)。
'''
def LohasBands(highs:pandas.Series, lows:pandas.Series, closes:pandas.Series, n:int=20) -> Iterable:
    if closes.shape[0] < 1: return empty_series(), empty_series(), empty_series()
    # 求出N日內的高低與收均值
    df = pandas.concat([highs, lows, closes], axis=1)
    df.columns = ['high','low','close']
    df['high-max'] = df['high'].rolling(n).max()
    df['low-min'] = df['low'].rolling(n).min()
    df['close-ma'] = round(df['close'].rolling(n).mean(), 2)
    # 求出振幅
    df['high-low'] = round(df['high'] - df['low'], 2)
    df['half'] = round((df['high'] + df['low']) / 2, 2)
    df['k'] = round(df['high-low'] / df['half'], 2)
    # 求高低區間
    df['up'] = round(df['high'] * (1 + 2 * df['k']), 2)
    df['dn'] = round(df['low'] * (1 - 2 * df['k']), 2)
    # 求高低區間N日均值
    df['up-ma'] = round(df['up'].rolling(n).mean(), 2)
    df['dn-ma'] = round(df['dn'].rolling(n).mean(), 2)
    #
    df.to_csv(f'{temp_path}/lbands.csv')
    return df['up-ma'], df['close-ma'], df['dn-ma']


'''
唐奇安通道 (Donchian Channel)
    唐奇安通道的上下軌計算方式為
    上軌為過去一段時間內的最高價
    下軌為過去一段時間內的最低價
    日內交易最常用的指標之一。市場波動越大，通道越寬，反之。

'''
def DonCH(highs:pandas.Series, lows:pandas.Series, closes:pandas.Series, n:int=20) -> Iterable:
    if closes.shape[0] < 1: return empty_series(), empty_series(), empty_series()
    df = pandas.concat([highs, lows, closes], axis=1)
    df.columns = ['high','low','close']
    df['up'] = df['high'].rolling(n).max()
    df['dn'] = df['low'].rolling(n).min()
    df['md'] = round((df['up'] + df['dn']) / 2, 2)
    #
    df.to_csv(f'{temp_path}/donch.csv')
    return df['up'], df['md'], df['dn']


