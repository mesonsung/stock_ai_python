
'''
爬蟲 crawler / 蜘蛛 spider
'''

# 作業系統模組
import os
# 正規表達式模組
import re
# 執行緒模組
import threading
# 時間模組
import time
# 隨機值模組
import random




# 函式::抓個股基本資料
# 參數
#   <str> sym 證券代碼
# 回傳
#   None
def crawler_info(sym:str) -> None:
    # 參數檢核
    if not re.match(r'^[0-9]{4}$', sym):
        print('sym 證券代碼不正確')
        return

    print('建立數據目錄 ./stocks')
    data_path = f'{__path__}/stocks'
    os.makedirs(
        data_path,
        0o755,
        exist_ok=True
    )

    # YAHOO 上市/櫃的尾碼有區別
    sym1 = f'{sym}.TW'  # 上市
    sym2 = f'{sym}.TWO' # 櫃
    sym_list = [sym1, sym2]

    for no in sym_list:
        # 隨機休息::避免被誤會是DDoS分散式阻斷服務攻擊
        time.sleep(random.randint(1, 5))

        print(f'爬取 {no} 個股的基本資料')
        # 匯入HTTP通訊模組
        import requests
        # API網址
        api_url = f'https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.symbolOverview;errorPolicy=all;showUpcoming=true;symbol={no}'
        # API參數
        api_param = f'?bkt=&device=desktop&ecma=modern&feature=ecmaModern%2CuseVersionSwitch%2CuseNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=d93cp99grqmj8&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.1207&returnMeta=true'
        # HTTP 請求標頭(將爬蟲偽裝成瀏覽器)
        headers = {
            'Referer': f'https://tw.stock.yahoo.com/quote/{sym}/institutional-trading',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57'
        }
        # 透過 HTTP GET 通訊方法進行遠端請求
        # 並將回應內容儲存在變數(記憶體) response 裡
        try:
            response = requests.get(
                url=f'{api_url}{api_param}',
                headers=headers
            )
            # 判斷回應狀態碼 200:正常
            if response.status_code == 200:
                # 200:正常
                jsonstr = response.text
                # 資料數據內容檢核
                # 轉換成 JSON 格式化結構物件
                import json
                jsonobj = json.loads(jsonstr)
                if 'errors' in jsonobj['data']:
                    # 有存在，回應的內容不是正確的
                    print(jsonobj['data']['errors'])
                else:
                    # 不存在，回應的內容是正確的
                    # 寫入到檔案 mode:'w'覆寫檔案內容,'a'將內容寫入到最末行
                    with open(
                        f'{data_path}/info_{sym}.json',
                        'w',
                        encoding='UTF-8'
                    ) as fw:
                        fw.write(jsonstr)
                    # 已經找到正確資料，脫離迴圈
                    break
            else:
                # 其他狀態碼
                print(f'HTTP狀態碼 {response.status_code}')
        except Exception as ex:
            print(ex)
    print('爬取資料完成')


# UI介面
def ui():
    while True:
        # 清除畫面
        os.system('cls')
        print('歡迎進入台股證券查詢系統\n')
        # 接收使用者輸入的字串
        sym = input('請輸入證券代碼[4碼] (q:結束): ')
        # 當用戶輸入Q/q表示結束，脫離迴圈
        if sym.lower() == 'q':
            break
        print('\n資料查詢中 ...')
        # 爬取該股基本資料
        crawler_info(sym)
        input('\n>>>> 按<ENTER>鍵繼續 ...')
    print('\n感謝您的使用')



# 切割多筆證券代碼
def split(syms:str) -> list:
    if not re.match(r'[0-9\s\,]+', syms):
        return None
    items = syms.split(',')
    items = [item.strip() for item in items]
    return items


# UI2介面
def ui2():
    while True:
        # 清除畫面
        os.system('cls')
        print('歡迎進入台股證券查詢系統\n')
        # 接收使用者輸入的字串
        sym = input('請輸入證券代碼[4碼，多筆用逗號,來區隔] (q:結束): ')
        # 當用戶輸入Q/q表示結束，脫離迴圈
        if sym.lower() == 'q':
            break
        # 將輸入的資料進行切割
        sym = split(sym)
        print('\n資料查詢中 ...')
        # 逐筆爬取該股基本資料
        for no in sym:
            # 委派給執行緒去處理，透過執行緒池統一管理
            t = threading.Thread(
                target=crawler_info,
                kwargs={'sym':str(no)}
            )
            pool.append(t)
            t.start()
    # 等候所有子執行緒全部執行完成
    for t in pool:
        t.join()
    input('\n>>>> 按<ENTER>鍵繼續 ...')
    print('\n感謝您的使用')


# UI3介面
def ui3():
    # 清除畫面
    os.system('cls')
    print('歡迎進入台股證券查詢系統\n')
    print('\n讀取 list.txt 名單')
    time.sleep(3)
    # 讀取檔案內容
    text = ''
    with open(
        f'{__path__}/list.txt',
        'r',
        encoding='UTF-8'
    ) as fr:
        text = fr.read()
    # 切割資料
    sym = split(text)
    print('\n資料查詢中 ...')
    # 逐筆爬取該股基本資料
    for no in sym:
        # 委派給執行緒去處理，透過執行緒池統一管理
        t = threading.Thread(
            target=crawler_info,
            kwargs={'sym':str(no)}
        )
        pool.append(t)
        print(f'{no} 開始作業 ...')
        t.start()
    # 等候所有子執行緒全部執行完成
    for t in pool:
        t.join()
    print('\n感謝您的使用')





print('目前執行腳本檔案路徑')
print(__file__)
# 專案目錄路徑
__path__ = os.path.dirname(__file__)
# 執行緒池
pool = list()

if __name__ == '__main__':
    ui2()
