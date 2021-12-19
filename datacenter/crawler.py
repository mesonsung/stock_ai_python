'''
網路爬蟲程式
'''

import os
import requests
import json
import re
import threading
'''
建立爬到資料後存放的路徑
__path__ : 當前專案執行的路徑
daily_path : 存放日線的資料夾
'''
# 專案目錄路徑
__path__ = os.path.dirname(__file__)
#print(__path__)
daily_path = f'{__path__}/daily'
info_path = f'{__path__}/info'
#建立目錄
os.makedirs(daily_path, mode=0o755, exist_ok=True)
os.makedirs(info_path, mode=0o755, exist_ok=True)

# 寫入到檔案
def save_data(response,file) -> None:
  with open(file, 'w', encoding='utf-8') as f:
    if 'application/json' in response.headers.get('content-type'):
      json_obj = response.json()
      if 'errors' in json_obj['data']:
        print(json_obj['data']['errors'])
      else:
        json.dump(json_obj, f, ensure_ascii=False, indent=4)
    else:
      f.write(response.text)

def check_sym(sym:str):
  # 正規表達式檢查
  if re.match(r'^[0-9]{4}$',sym):
    return True
  else:
    return False

def crawler_info(sym:str,type="") -> None:
  # 檢查參數
  if check_sym(sym) == False:
    print(f'股票代碼[{sym}]錯誤！')
    return
  # API URL
  api_url = f'https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.symbolOverview;errorPolicy=all;showUpcoming=true;symbol={sym}.TW{type}'
  # API 參數
  api_params = '?bkt=&device=desktop&ecma=modern&feature=ecmaModern%2CuseVersionSwitch%2CuseNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=d93cp99grqmj8&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.1207&returnMeta=true'
  # 將爬蟲偽裝成瀏覽器
  headers = {
      'Referer': f'https://tw.stock.yahoo.com/quote/{sym}/institutional-trading',
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
  }
  # 呼叫API取得資料
  print(f'開始爬取股粟[{sym}] ...')
  response = requests.get(
      url=f'{api_url}{api_params}',
      headers=headers
  )
  # 判斷回應碼
  if response.status_code == requests.codes.ok:
    save_data(response,f'{info_path}/{sym}.json')
    print(f'股票代碼[{sym}]爬取資料完成囉！')
  else:
      response.raise_for_status()

def split_syms(syms:str)->list:
  items = syms.split(',')
  items = [item.strip() for item in items]
  return items

# UI介面
def ui():
    pool=list()
    while True:
        # 清除畫面
        os.system('clear')
        print('歡迎進入台股證券查詢系統 !\n')
        # 接收使用者輸入的字串
        imput_sym = input('請輸入證券代碼[4碼] (q:結束): ')
        # 當用戶輸入Q/q表示結束，脫離迴圈
        if imput_sym.lower() == 'q':
            break

        syms = split_syms(imput_sym)
        print('\n資料查詢中 ...')
        # 爬取該股基本資料
        for sym in syms: 
          t = threading.Thread(
            target=crawler_info,
            kwargs={'sym':sym,"type":""}
          )
          #crawler_info(sym)
          pool.append(t)
          t.start();
        for t in pool:
          t.join()
        input('\n>>>> 按<ENTER>鍵繼續 ...')
        pool.clear()
    print('\n感謝您的使用')


if __name__ == '__main__':
  # 上市股票代碼
  #crawler_info('2603',"")
  # 上櫃股票代碼
  #crawler_info('3105',"O")
  ui()
