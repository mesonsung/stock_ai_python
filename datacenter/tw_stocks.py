# -*- coding: utf-8 -*-
'''
Program    : 台灣證交所商品代碼表
Author     : 從天慶
Created    : 2021-01-01
Version    : 1.0.0
Description: 數據來自於台灣證交所 www.twse.com.tw
'''


'''
證券代碼公告
https://isin.twse.com.tw/isin/C_public.jsp?strMode=2

strMode 證券分類表代碼
    1: 本國未上市，未上櫃公開發行證券，國際證券辨識號碼一覽表
    2: 本國上市證券國際證券辨識號碼一覽表
    3: 本國上市債券，上櫃債券，國際證券辨識號碼一覽表
    4: 本國上櫃證券國際證券辨識號碼一覽表
    5: 本國興櫃證券國際證券辨識號碼一覽表
    6: 本國期貨及選擇權國際證券辨識號碼一覽表
    7: 本國開放式證券投資信託基金，國際證券辨識號碼一覽表
    8: 本國未公開發行之創櫃板證券國際證券辨識號碼一覽表
    9: 登錄買賣黃金現貨國際證券辨識號碼一覽表
    10: 外幣計價可轉換定期存單，國際證券辨識號碼一覽表
    11: 本國指數國際證券辨識號碼一覽表
    12: 虛擬通貨STO，國際證券辨識號碼一覽表
'''


'''
第三方套件模組  https://pypi.org

    HTTP 通訊模組
    requests 2.26.0
        pip install requests==2.26.0
        pip install --upgrade requests==2.26.0

    大數據操作與分析模組
    pandas 1.3.5
        pip install pandas==1.3.5
        pip install --upgrade pandas==1.3.5
'''




# 作業系統模組
import os
# HTTP 通訊模組
import requests
# 大數據操作與分析模組
import pandas


# 設定專案路徑
__path__ = os.path.dirname(__file__)



# 函數::獲取HTML原始碼
# 參數
#   <int> 證券分類表代碼: 1~12
# 回傳
#   <str>
def fetch_html_from_mode(mode:int) -> str:
    # 資料檢核
    if type(mode) != int: raise Exception('mode error, range: 1 ~ 12')
    if mode < 1 or mode > 12: raise Exception('mode error, range: 1 ~ 12')
    # HTTP 請求標頭
    request_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57',
        'Referer': 'https://www.twse.com.tw/zh/page/products/stock-code2.html'
    }
    # HTTP 請求作業
    response = requests.get(
        f'https://isin.twse.com.tw/isin/C_public.jsp?strMode={mode}',
        headers=request_headers
    )
    # 判斷回應碼
    if response.status_code == 200:
        # 正常代碼，回傳內容
        return response.text
    else:
        # 其他代碼
        return ''



# 函數::獲取上市與上櫃的股票代碼
# 參數
#   <bool> use_remote   是否使用遠端資料?
#   <bool> save_csv     是否儲存CSV檔?
#   <bool> save_html    是否儲存HTML檔?
# 回傳
#   <pandas.DataFrame>
def fetch_tw_stocks(
    use_remote:bool=False,
    save_csv:bool=False, save_html:bool=False) -> pandas.DataFrame:

    # 資料目錄
    data_path = f'{__path__}/stocks/'

    # 新表格
    columns = ['no', 'title', 'industry', 'market', 'publish', 'delisted']
    df_new = pandas.DataFrame(columns=columns)

    # 證券分類表代碼集合
    modes = [2, 4]
    # 逐筆爬取
    for i in range(len(modes)):
        mode = modes[i]
        html = ''
        # 本地端HTML檔案路徑
        html_file = f'{data_path}/tw_stocks_{mode}.html'
        # 當本地端檔案不存在或是強制從遠端下載時
        if not os.path.isfile(html_file) or use_remote:
            # 下載並存檔
            html = fetch_html_from_mode(mode)
            if save_html:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html)
        else:
            # 從本地端檔案讀取
            with open(html_file, 'r', encoding='utf-8') as f:
                html = f.read()

        # 使用 pandas 進行數據清洗作業
        # 讀取 HTML 原始碼轉換成 pandas.DataFrame
        df = pandas.read_html(html)[0]
        # 設定標題欄位
        df.columns = df.loc[0]
        # 篩出上市股票
        df = df[df['CFICode']=='ESVUFR']
        # 處理代碼與名稱，並產生新的欄位
        df['證券代號'] = df['有價證券代號及名稱'].apply(lambda v: str(v)[0:4])
        df['證券名稱'] = df['有價證券代號及名稱'].apply(lambda v: str(v)[4:].strip())
        df['移除標示'] = 'N'
        # 重取欄位
        df = df[['證券代號', '證券名稱', '產業別', '市場別', '上市日', '移除標示']]
        # 重新命名欄位
        df.columns = columns

        # 匯入
        df_new = df_new.append(df)

        # 儲存到CSV
        if save_csv:
            # 預設新檔案寫入
            mode = 'w'
            header = True
            # 當有第二個表格時，改用附加寫入不帶標題列
            if i > 0:
                mode = 'a'
                header = False
            # 寫入CSV檔
            df.to_csv(
                f'{data_path}/tw_stocks.csv',
                index=False,
                quoting=1,
                mode=mode,
                header=header
            )
    # 回傳
    return df_new



if __name__ == '__main__':
    print('從證交所取得上市櫃證券代碼')
    df = fetch_tw_stocks(save_csv=True)
    print(df)