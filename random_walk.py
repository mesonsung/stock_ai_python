#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
【練習作業】
我們需要產生一個隨機常態的股價漲跌模擬數據
因此，利用隨機漫步原理來進行小規模的實作
待實作成功，再封裝成函數，供日後可以重複使用，無須每次重寫演算法

=============================================================

【原理運用】
演算法 :: 隨機漫步 Random Walk
演算概念:
    每前進一步的方向(假設方向限定在往右上與往右下兩種)是種隨機。
    每前進一步的步伐長度(具有合理的限定範圍)也是種隨機。
    這就是隨機漫步的思維原理。
    將隨機的每一步連接起來，就尤如隨興常態般的行徑軌跡。
概念應用:
    股價/指數，每一天都會有漲跌方向與漲跌幅度。
    如同隨機漫步般，構成了一條隨興常態般的行徑軌跡。
演算原理:
    1. 隨機漫步的過程裡，需要知道「起點位置與途程終點」
    2. 過程是逐步執行
    3. 每次執行都會產生「隨機的行徑方向與步伐長度」
    4. 將目前所在的位置，依「隨機的行徑方向與步伐長度」產生新的前進位置

=============================================================

【模組資源】
Python 有許多的功能模組(Module)，其中的 random 模組（內建模組）具有隨機亂數的各種產生方法
    random.randint(low, high) 依限定範圍產生隨機整數
    random.uniform(low, high) 依限定範圍產生隨機浮點數

Python 安裝擴充模組 CLI 指令
C:\> pip install <擴充模組名稱>

函式 range(start, end, [step=1]) 會產生一個範圍結構，是專門用於計數迴圈 for in
參數 start:起始值; end:終止值(N-1); step:遞增值(預設+1，也可以是-1)
例如，從 0 輸出到 4
    for i in range(0, 5):
        print(i)

Python 字串格式化，以更清晰簡潔的方式組合「字串型態的變數與字串」
語法: '格式化字串' % (變數1, 變數2, ...)
常見代數符號:
    %s 文字型態<class 'str'>變數
    %d 整數型態<class 'int'>變數
    %f 浮點數型態<class 'float'>變數，%.2f 表示取到小數第二位
例如:
    print('姓名:%s 年齡:%d 體質指數(BMI):%.1f', name, age, bmi)
'''


'''
請將下列的註解開頭為 Python:: 的下一行翻譯為程式碼
請翻閱教材或上教學網站充分理解 Python 語言知識
'''

# Code::匯入 random 模組

import csv
import random
import datetime
import os
def save_data(data):
    # 開啟輸出的 CSV 檔案
    output_path = '%s/output' % os.path.abspath(os.getcwd())
    isExist = os.path.exists(output_path)
    if(isExist == False):
        os.mkdir(output_path)
    filename = '%s/%s.csv' % (output_path, datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S"))
    print(filename)
    with open(filename, 'w', newline='') as csvfile:
        # 定義欄位
        fieldnames = ['date', 'weekday', 'price']

        # 將 dictionary 寫入 CSV 檔
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 寫入第一列的欄位名稱
        writer.writeheader()

        # 寫入資料
        for item in data:
            writer.writerow(item)
    pass


def generate_data(init_price=15, data_days=20, save=False):
    # 起始股價
    # Code::宣告名為 price 的變數，初始值指派為 15
    price = init_price

    # 交易天數
    # Code::宣告名為 days 的變數，初始值指派為 20
    days = data_days

    # 依交易天數產生隨機漫步的股價
    # Code::計數迴圈::範圍 0 至 20
    generated_data = list()
    start_date = datetime.datetime.now() - datetime.timedelta(days=data_days+1)
    current_date = start_date
    delta_day = datetime.timedelta(days=1)
    for day in range(1, days+1, 1):
        # 隨機產生漲跌方向，1:漲; -1:跌
        # Code::宣告名為 step 的變數(漲跌方向)，初始值為隨機值，範圍 0 至 1
        # step = random.randrange(0,2,1)
        #step = 1 if random.randrange(0, 2, 1) else -1
        step = (-1,1)[random.randint(0,1)]
        # Code::判斷 step 變數，若內容值符合 0 時表示條件成立
        # if step == 0:
        #     # Code::條件成立時，將 step 變數，內容值指派為 -1
        #     step = -1
        # 隨機產生漲跌幅度，台股最大漲跌幅度限制為 +/- 10%
        # Code::宣告名為 wave 的變數(幅度)，初始值為隨機值，範圍 0.02 至 0.1
        wave = random.uniform(0.02, 0.1)
        # 依前次的股價，計算隨機漲跌幅度
        # Code::將運算式 price * wave * step 的運算結果，指派給 wave 變數
        wave = price * wave * step
        # 將前次的股價加上隨機漲跌幅度
        # Code::將運算式 price + wave 的運算結果，指派給 price 變數
        price = price + wave
        # 儲存產生的資料
        day_data = dict()
        current_date = current_date + delta_day
        day_data['date'] = current_date.strftime("%Y-%m-%d")
        day_data['weekday'] = current_date.isoweekday()
        day_data['price'] = price
        generated_data.append(day_data)
        # 輸出隨機漫步的股價漲跌歷程
        # Code::格式化字串 '第 %d 天，價格 %.2f 元，漲跌幅 %.2f 元'，並依序套用變數 i + 1 、 price 與 wave
        # print('%s : 第 %d 天，價格 %.2f 元，漲跌幅 %.2f 元' %(day_data['date'], day, price, wave))
    if(save == True):
        save_data(generated_data)

    return generated_data


if __name__ == '__main__':

    data = generate_data(100, 100, True)
