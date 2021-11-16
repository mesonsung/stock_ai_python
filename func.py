'''
Program     : 函數庫
Author      : Meson
Created     : 2021-11-14
Version     : 1.0.0
Description : 程式化交易當用的函式
'''
#!/usr/bin/python
# -*- coding: utf-8 -*-
# 避免中文註解，造成編譯出問題

# 簡單平均法（均線）
# 參數：
#   prices：價格的集合(分／日／週／月線)
#   prep：頻率


def MA(prices, prep):
    # Step1. 判斷 prices 裡的價格集合內的資料是否都是數值
    for price in prices:
        # 透過type()來檢查prices裡的價格資料是否都為整數的數值(int/float)
        # 當發生資料型態不符合int 或是 float時，回傳 False 來中止運算
        if ((type(price) != int) and (type(price) != float)):
            return False
    # Step2. 判斷 prices 裡的價格集合內的資料是否達到prep可以計算的筆數
    # 數量低於可計算的筆數，回傳 False 來中止運算
    if len(prices) < prep:
        return False

    ma = 0
    count = 0
    for i in [*range(0,prep+1)]:
        # Step3. 依頻率取出資料範圍
        r = prices[i:prep+i]
        # Step4. 加總依頻率取出的資料
        sum = 0
        for price in r:
            sum=sum+price
        avg = sum / prep
        # Step5. 加總平均值
        ma = ma+avg
        # Step6. 記錄加總平均值的次數
        count = count +1
    # 算出移動平均值
    ma = ma / count
    return ma


# 黃金交叉（盤整趨勢方向不明，突破上方壓力，未來可能呈現（牛市）多方漲幅趨勢）
# 交易方式：多單交易（低價買進->高價賣出）
#   prices：目前的價格集合(分／日／週／月線)
#   line：比對用的價格集合（某個技術指標）
def CrossOver(prices, line):
    # 判斷 prices 裡的價格集合內的資料是否都是數值
    pass

# 死亡交叉（盤整趨勢方向不明，跌破下方支撐，未來可能呈現（熊市）空方跌幅趨勢）
# 交易方式：空單交易（高價賣出->低價買回）
#   prices：目前的價格集合(分／日／週／月線)
#   line：比對用的價格集合（某個技術指標）


def CrossBelow(prices, line):
    # 判斷 prices 裡的價格集合內的資料是否都是數值
    pass


# ----------------------------------------------------------------------
# 收盤價格集合
closed_prices = [1,2,3,4,5,6,7,8,9,10]

result = MA(closed_prices, 5)
print(result)
