# -*- coding: utf-8 -*-
'''
Program    : 均線交叉策略模擬
Author     : 從天慶
Created    : 2021-11-14
Version    : 1.0.0
Description: 運用均線與交叉來判斷可能的多空走勢
'''


# 給同學們的作業
'''
技術文件參考:
    菜鳥教程 Python3         : https://www.runoob.com/python3/python3-tutorial.html
    Python 函數可變參數       : https://blog.maxkit.com.tw/2018/12/python-args-kwargs.html
    Python 3.8 官網文件      : https://docs.python.org/3.8/
    Matplotlib 讓資料視覺化！ : https://ithelp.ithome.com.tw/articles/10196239
    Matplotlib 套用中文字型   : https://pyecontech.com/2020/03/27/python_matplotlib_chinese/
    Matplotlib 官網文件      : https://matplotlib.org/stable/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py

作業須知:
    1. 請同學們反覆地練習，將主程序以及每個函式的流程翻譯成口語化的流程描述，在適當位置去註解。
        1-1. 試圖去理解每一行指令的意義與為何要這樣去寫
        1-2. 語法部分，請參考技術文件去了解其用途與用法，並試著小規模練習。
        1-3. 透過中斷點，去觀察整個應用程序的執行過程(變數、堆疊)，某些運算式可加入到「監看」去預覽運算結果。
        1-4. 多去上網查閱學習，用關鍵字 python 再加上你想問的問題。學會怎麼問，很重要。
    2. 當熟悉流程後，請依本案例試著從無到有撰寫一個 Python 腳本檔案。
        2-1. 註解很重要。
        2-2. 撰寫的過程裡，可以試著去找出最佳的寫法。
    3. 若有學過其它程式語言的同學，可以試著用其它程式語言依本案例來實作，比較其語言的差異。
    4. 下次上課要展示給老師看你的學習成果。
    5. 試著將本檔案透過 import 方式匯入到另一個 Python 檔案裡當模組來使用。
    6. 學習上有任何問題，先試著自己去找出問題並解決。
        6-1. 萬不得已時，再去向指導員請教。
        6-2. 找出問題並解決，這也是基本功練除錯經驗！
    7. 若已經對撰寫程式開竅的同學，可以試著去理解並實作課本裡的案例。
'''



# 匯入必要模組
'''
模組(Module)的用途就是將相同性質的函式(Function)給群組化(Group)，
以利開發人員利於用途辨識與使用。
Python 模組化的方式，是利用腳本檔案本身來當作模組 <模組名稱>.py
例如：有一個技術指標模組 indicator.py 檔案內定義了許多分析用的技術指標

腳本檔案 indicator.py
--------------------

# 簡單移動平均 Simple Moving Average
def SMA(data, prep):
    pass

# 乖離率 Bias
def BIAS(a, b):
    pass

# 指數平滑異同移動平均 Moving Average Convergence / Divergence
def MACD(data, prepFast, prepSlow):
    pass

# 隨機指標 Stochastic Oscillator
def KD(data, prepFast, prepSlow, prepDiff):
    pass

# 相對強弱指標 Relative Strength Index
def RSI(data, prepFast, prepSlow):
    pass

...(省略)
'''
# 正規表達式模組
import re
# 日期時間模組
import datetime
# 隨機值模組
import random
from random_walk import generate_data


# -------------------------------------------------------------


# 轉換成西元日期字串
#   參數:
#       strdate:日期字串(格式:YYYY-mm-dd, YYYY/mm/dd, YYYY.mm.dd, YYYYmmdd)
#   回傳:
#       str:日期字串 / None:不符合日期格式時
def parse_date_str(strdate):
    if type(strdate) != str:
        return None
    re_pattern = '^[0-9]{4}[-\/\.][0-9]{2}[-\/\.][0-9]{2}$'
    if re.match(re_pattern, strdate):
        return strdate
    re_pattern = '^[0-9]{8}$'
    if re.match(re_pattern, strdate):
        return '%s-%s-%s' % (strdate[0:4], strdate[4:6], strdate[6:])
    return None

# -------------------------------------------------------------

# 隨機產生日線資料
# 參數:
#   start_date: 起始日期
#   days: 天數
# 回傳:
#   list(dict(), dict(), ...)
#       dict 預設資料結構: {'date':'日期(格式:YYYY-mm-dd)', 'weekday':'星期(範圍:1~5)', 'price':'價格或指數'}
def random_data(start_date = '2021-01-01', days = 22):
    start_date = parse_date_str(start_date)
    current_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    data = list()
    day_i = 1
    while (day_i <= days):
        current_date = current_date + datetime.timedelta(days = 1)
        weekday = current_date.isoweekday()
        if (weekday >= 1 and weekday <= 5):
            # print(current_date.strftime('%Y-%m-%d (%w)'))
            item = dict()
            item['date'] = current_date.strftime('%Y-%m-%d')
            item['weekday'] = weekday
            item['price'] = random.randrange(15000, 18000)
            data.append(item)
            day_i = day_i + 1
    return data

# -------------------------------------------------------------

# 簡單移動平均線
# 參數:
#   data: 日線資料集合
#   prep: 頻率
# 回傳:
#   True: 執行完成
def SMA(data, prep = 5):
    for i in range(0, len(data)):
        attr_ma = 'sma%d' % (prep)
        if i < prep:
            data[i][attr_ma] = None
        else:
            avg = 0
            items = data[i - prep : i]
            for item in items:
                avg = avg + item['price']
            avg = round(avg / prep)
            data[i][attr_ma] = avg
    return True

# -------------------------------------------------------------

# 是否為數值
#   參數:
#       value: 欲檢測的資料值
#   回傳:
#       True:數值 / False:非數值
def IsNumber(value):
    return type(value) == int or type(value) == float

# -------------------------------------------------------------

# 黃金交叉
#   參數:
#       a: 主要資料
#       b: 比對用資料
#   回傳:
#       True:穿越突破向上 / False:無
def CrossOver(a, b):
    if not IsNumber(a) or not IsNumber(b):
        return False
    return a > b

# -------------------------------------------------------------

# 死亡交叉
#   參數:
#       a: 主要資料
#       b: 比對用資料
#   回傳:
#       True:穿越跌破向下 / False:無
def CrossBelow(a, b):
    if not IsNumber(a) or not IsNumber(b):
        return False
    return a < b

# -------------------------------------------------------------

# ISO星期轉換成中文
# 參數:
#   w: ISO星期(1~7)
# 回傳:
#   str: 中文星期
def isoweekday_to_chinese(w):
    if (type(w) != int):
        return None
    if (w < 1 or w > 7):
        return None
    chineses = ['一', '二', '三', '四', '五', '六', '日']
    return chineses[w - 1]

# -------------------------------------------------------------

# 將集合內的字典元素依指定的字典鍵名轉換成集合
# 參數:
#   list_dict: 存放著 dict() 字典元素的集合
#   dict_key: 鍵名
# 回傳:
#   list():集合 / None:無
def dict_attr_to_list(list_dict, dict_key):
    if type(list_dict) != list:
        return None
    if type(dict_key) != str and dict_key == '':
        return None
    if len(list_dict) < 1:
        return None
    if not dict_key in list_dict[0]:
        return None
    items = list()
    for item in list_dict:
        if (type(item) != dict):
            return None
        else:
            items.append(item[dict_key])
    return items

# -------------------------------------------------------------

# 繪製圖表
# 參數:
#   x: X軸資料集合
#   y: Y軸資料集合
# 回傳:
#   無
def draw_plot(option,file_name):
    # 取得中文字型目錄位置
    import os
    from pathlib import Path
    font_path = __file__.replace(os.path.basename(__file__), '')
    font_path = Path(font_path, 'font')
    # 將中文字型目錄位置載入到 matplotlib 字型管理員內
    import matplotlib.font_manager as fmgr
    font_dirs = [font_path]
    font_files = fmgr.findSystemFonts(fontpaths=font_dirs)
    for font in font_files:
        fmgr.fontManager.addfont(font)
    
    # matplotlib 套用中文字型
    import matplotlib.pyplot as plt
    plt.rcParams['font.family'] = 'Taipei Sans TC Beta'
    # 設定圖表標題
    if 'title' in option:
        plt.title(option['title'])
    # 設定X軸標題
    if 'xLabel' in option:
        plt.xticks(fontsize=8, rotation=90)
        plt.xlabel(option['xLabel'])
    # 設定Y軸標題
    if 'yLabel' in option:
        plt.ylabel(option['yLabel'])

    # 圖表資料數據集合
    lines = []
    # 圖表資料項目名稱集合
    legends = list()
    # 彙整資料
    for item in option['y']:
        lines.append(option['x'])
        lines.append(item['data'])
        legends.append(item['name'])
    # 產生 plot() 參數集合，利用 * 符號(記憶體指標的方式)來傳遞參數
    lines = plt.plot(*lines)

    # 設定圖表資料數據集合
    plt.setp(lines, marker='')
    # 設定圖表資料項目名稱集合
    plt.legend(legends)

    # 顯示格線
    plt.grid(True)
    # 顯示互動圖表介面
    if file_name!="":
        plt.savefig(file_name)
    plt.show()

# -------------------------------------------------------------

# 當 ma_cross.py 腳本透過 Python 直譯器給直接執行時 python.exe ma_cross.py
# 則此腳本的模組名稱為 __main__ ，表示應用程序的主程序(也就是堆疊區裡的第一個函式)
if __name__ == '__main__':
    print('主程序開始 ----------------------------')
    
    # data = random_data(days = 66)
    params=dict();
    params['init_price'] = 100
    params['data_days'] = 100
    params['max_wave'] = 0.1
    params['save'] = False
    csv_file, data = generate_data(**params)
    # print(data)

    SMA(data, 5)
    SMA(data, 10)
    SMA(data, 20)
    # print(data)

    for item in data:
        date  = '%s (%s)' % ( item['date'], isoweekday_to_chinese(item['weekday']) )
        price = item['price']
        sma5   = item['sma5']
        sma10  = item['sma10']
        sma20  = item['sma20']

        if CrossOver(item['price'], sma5):
            print('%s 價格 %d 與 SMA5 五日(周)均線 %d 呈現黃金交叉' % (date, price, sma5))
        if CrossOver(item['price'], sma10):
            print('%s 價格 %d 與 SMA10 十日(半月)均線 %d 呈現黃金交叉' % (date, price, sma10))
        if CrossOver(item['price'], sma20):
            print('%s 價格 %d 與 SMA20 二十日(月)均線 %d 呈現黃金交叉' % (date, price, sma20))
        if CrossBelow(item['price'], item['sma5']):
            print('%s 價格 %d 與 SMA5 五日(周)均線 %d 呈現死亡交叉' % (date, price, sma5))
        if CrossBelow(item['price'], item['sma10']):
            print('%s 價格 %d 與 SMA10 十日(半月)均線 %d 呈現死亡交叉' % (date, price, sma10))
        if CrossBelow(item['price'], item['sma20']):
            print('%s 價格 %d 與 SMA20 二十日(月)均線 %d 呈現死亡交叉' % (date, price, sma20))


        if CrossOver(sma5, sma10):
            print('%s SMA5(%d), SMA10(%d) 二均線上揚，呈現短多趨勢' % (date, sma5, sma10))
        if CrossBelow(sma5, sma10):
            print('%s SMA5(%d), SMA10(%d) 二均線下彎，呈現短空趨勢' % (date, sma5, sma10))


        if CrossOver(sma5, sma10) and CrossOver(sma10, sma20):
            print('%s SMA5(%d), SMA10(%d), SMA20(%d) 三均線上揚，呈現多方趨勢' % (date, sma5, sma10, sma20))
        if CrossBelow(sma5, sma10) and CrossBelow(sma10, sma20):
            print('%s SMA5(%d), SMA10(%d), SMA20(%d) 三均線下彎，呈現空方趨勢' % (date, sma5, sma10, sma20))

    _dates  = dict_attr_to_list(data, 'date')
    _prices = dict_attr_to_list(data, 'price')
    _sma5s  = dict_attr_to_list(data, 'sma5')
    _sma10s = dict_attr_to_list(data, 'sma10')
    _sma20s = dict_attr_to_list(data, 'sma20')

    plot_option = {
        'title': '日線圖',
        'xLabel': '日期',
        'yLabel': '價格/指數',
        'x': _dates,
        'y': [
            {
                'name': '價格/指數',
                'data': _prices
            },
            {
                'name': 'SMA5',
                'data': _sma5s
            },
            {
                'name': 'SMA10',
                'data': _sma10s
            },
            {
                'name': 'SMA20',
                'data': _sma20s
            },
        ]
    }
    file_name = csv_file.replace('csv','png')
    draw_plot(plot_option,file_name)
    
    print('主程序結束 ----------------------------')