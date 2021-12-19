'''
數據中心 Data Center
    為了長期的量化交易需求，得自行建置一個數據中心。
    主要功能有定期數據來源下載、數據清洗、數據管理與數據存取。
    我們這次會使用 Yahoo Finance (美國與台灣) 作為數據來源。
    在不考慮使用資料庫軟體前提下，如何做好資料管理
    資料中心收集的數據有：
        個股
            基本資料
            交易資料(1分/1日)
            籌碼資料
            股利資料
            財務資料


這次，我們以股市為主題，以兩種數據來實作練習
    1. 個股基本資料
    2. 個股每日的交易資料 OHLCV
    


目錄架構
    ./                                          專案目錄
        stocks/                                 資料中心
            tw_stocks.csv                       台灣上市櫃證券代碼檔
            <sym_no>/                           個股目錄
                info_<sym_no>.json              個股基本資料檔
                daily_<sym_no>.csv              日線資料
                ---------------------------------------------------
                minutes/                        分線目錄
                    minute_<sym_no>_<Ymd>.csv   分線資料



數據爬蟲設計
    台灣YAHOO股市數據爬取，採用多執行緒方式設計。
    為避免被伺服器列為 DDoS 分散式阻斷服務攻擊 (distributed denial-of-service attack)。
    將每個執行緒隨機暫停 1~3 秒。
    執行緒數量預設 10 個，請斟酌電腦效能、網路效能與伺服器存取情況調整之。



第三方套件模組 https://pypi.org

    大數據操作與分析模組
    pandas 1.3.5
        pip install pandas==1.3.5
        pip install --upgrade pandas==1.3.5

    美國YAHOO股市數據模組(需隨時關注是否有更新，避免抓不到資料)
    yfinance 0.1.67
        pip install yfinance==0.1.67
        pip install --upgrade yfinance==0.1.67

    HTTP 通訊模組
    requests 2.26.0
        pip install requests==2.26.0
        pip install --upgrade requests==2.26.0
'''


# 作業系統模組(內建)
import os
# 時間模組(內建)
import time
# JSON模組(內建)
import json
# 執行緒模組(內建)
import threading
# 隨機值模組(內建)
import random
# 大數據操作與分析模組
import pandas
# 美國股市數據模組
import yfinance
# HTTP 通訊模組
import requests



# 設定專案路徑
__path__ = os.path.dirname(__file__)



# 類別::數據中心
class DataCenter:
    # 私有屬性::資料目錄路徑
    __data_path:str = ''
    # 私有屬性::上市櫃證券代碼表
    __stocks:pandas.DataFrame = None
    # 私有屬性::上市櫃證券代碼表CSV檔案路徑
    __stocks_csv_file:str = ''
    # 類別實體化建構式
    def __init__(self) -> None:
        self.__check_data_path()
        self.__load_stocks()
    # 私有方法::檢查資料目錄
    def __check_data_path(self) -> None:
        self.__data_path = f'{__path__}/stocks/'
        os.makedirs(self.__data_path, 0o755, exist_ok=True)
    # 私有方法::載入上市櫃證券代碼表
    def __load_stocks(self) -> None:
        self.__stocks_csv_file = f'{self.__data_path}/tw_stocks.csv'
        if os.path.isfile(self.__stocks_csv_file):
            self.__stocks = pandas.read_csv(self.__stocks_csv_file)
    # 公開屬性::上市櫃證券代碼表
    @property
    def stocks(self) -> pandas.DataFrame:
        return self.__stocks
    # 私有方法::取得待更新的日線名單
    # 參數
    #   <str> keyname 檔案字首識別名稱
    def __get_upgrade_list(self, keyname:str) -> None:
        if not keyname: return
        df = self.__stocks
        df = df[df['delisted']=='N']
        upgrade_list = list(df['no'].apply(str))
        now = time.strftime('%Y-%m-%d', time.localtime())
        base_path = f'{__path__}/stocks/'
        dirs = os.listdir(base_path)
        for d in dirs:
            p = f'{base_path}/{d}/'
            f = ''
            fcsv = f'{p}/{keyname}_{d}.csv'
            fjson = f'{p}/{keyname}_{d}.json'
            if os.path.isfile(fcsv): f = fcsv
            if os.path.isfile(fjson): f = fjson
            if os.path.isfile(f):
                # 取得檔案資訊
                f_stat = os.stat(f)
                # 容量
                size = f_stat.st_size
                # 最後修改日期
                modifyymd = time.strftime('%Y-%m-%d', time.localtime(f_stat.st_mtime))
                # 已經更新過的從清單內移除
                if d in upgrade_list:
                    if f == fcsv:
                        if size > 100000 and modifyymd == now:
                            upgrade_list.remove(d)
                    else:
                        if modifyymd == now:
                            upgrade_list.remove(d)
        return upgrade_list
    # 公開方法::從證券代碼表來更新日線資料
    # 參數
    #   <int> n 每次更新的項目數量
    def upgrade_daily_ohlcv_from_stocks(self, n:int=10) -> None:
        # 取得更新名單
        upgrade_list = self.__get_upgrade_list('daily')
        if (len(upgrade_list) < 1): return
        # 將證券代碼轉換成YAHOO專用代碼
        upgrade_list = [f'{w}.TW' for w in upgrade_list]
        # 更新作業
        i = 0
        c = len(upgrade_list)
        while i < c:
            stocks = upgrade_list[i:i+n]
            sheets = yfinance.download(stocks, group_by='tickers', auto_adjust=True, actions=True)
            for sym in stocks:
                no = sym.replace('.TW', '')
                csv_file = f'{self.__data_path}/{no}/daily_{no}.csv'
                os.makedirs(os.path.dirname(csv_file), exist_ok=True)
                sheets[sym].to_csv(csv_file)
            i = i + 10
            time.sleep(5)
    # 公開方法::更新日線資料
    # 參數
    #   <str> no 證券代碼
    def upgrade_daily_ohlcv(self, no:str) -> None:
        if not no: return
        sym = f'{no}.TW'
        sheet = yfinance.Ticker(sym)
        sheet = sheet.history(period='max', interval='1d')
        csv_file = f'{self.__data_path}/{no}/daily_{no}.csv'
        os.makedirs(os.path.dirname(csv_file), exist_ok=True)
        sheet.to_csv(csv_file)
    # 公開方法::將有問題的項目進行移除標示
    def upgrade_mask_delisted(self) -> None:
        # 取得更新名單
        upgrade_list = self.__get_upgrade_list('daily')
        if len(upgrade_list) < 1: return
        upgrade_list = [int(w) for w in upgrade_list]
        # 比對並更新
        df = self.__stocks
        df['delisted'] = df['no'].apply(lambda v: 'Y' if v in upgrade_list else 'N')
        df.to_csv(self.__stocks_csv_file, index=False, quoting=1)
    # 公開方法::取得日線資料
    # 參數
    #   <str> no 證券代碼
    # 回傳
    #   <pandas.DataFrame>
    def get_daily_ohlcv(self, no:str) -> pandas.DataFrame:
        csv_file = f'{self.__data_path}/{no}/daily_{no}.csv'
        if os.path.isfile(csv_file):
            df = pandas.read_csv(csv_file)
            df.index = pandas.to_datetime(df['Date'])
            return df
        else:
            return None
    # 私有方法::儲存文字檔
    # 參數
    #   <str> filename 檔案路徑
    #   <str> text 文字內容
    def __save_to_txt(self, filename:str, text:str) -> None:
        with open(filename, 'w', encoding='UTF-8') as fw:
            fw.write(text)
    # 私有方法::讀取文字檔
    # 參數
    #   <str> filename 檔案路徑
    def __read_from_txt(self, filename:str) -> str:
        text = ''
        with open(filename, 'r', encoding='UTF-8') as fr:
            text = fr.read()
        return text
    # 公開方法::更新基本資料
    # 參數
    #   <str> no 證券代碼
    def upgrade_info(self, no:str) -> None:
        if not no: return
        time.sleep(random.randint(1, 3))
        # 時間戳記 1594819641.9622827 秒 => 毫秒
        ts = round(time.time() * 1000)
        url = f'https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.symbolOverview;errorPolicy=all;showUpcoming=true;symbol={no}.TW'
        url = f'{url}?bkt=&device=desktop&ecma=modern&feature=ecmaModern%2CuseVersionSwitch%2CuseNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=d93cp99grqmj8&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.1207&returnMeta=true'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Referer': f'https://tw.stock.yahoo.com/quote/{no}/institutional-trading'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            p = f'{self.__data_path}/{no}'
            f = f'{p}/info_{no}.json'
            os.makedirs(p, 0o755, exist_ok=True)
            self.__save_to_txt(f, response.text)
    # 公開方法::取得個股基本資料
    # 參數
    #   <str> no 證券代碼
    # 回傳
    #   <str> JSON
    def get_info(self, no:str) -> str:
        json_file = f'{self.__data_path}/{no}/info_{no}.json'
        if os.path.isfile(json_file):
            text = self.__read_from_txt(json_file)
            return json.loads(text)
        else:
            return ''
    # 公開方法::從證券代碼表來更新個股基本資料
    # 參數
    #   <int> n 每次更新的項目數量
    def upgrade_info_from_stocks(self, n:int=10) -> None:
        # 取得更新名單
        upgrade_list = self.__get_upgrade_list('info')
        if (len(upgrade_list) < 1): return

        # 更新作業
        i = 0
        c = len(upgrade_list)
        pool = list()
        while i < c:
            stocks = upgrade_list[i:i+n]
            for no in stocks:
                t = threading.Thread(target=self.upgrade_info, kwargs={'no':no})
                pool.append(t)
                t.start()
            for t in pool:
                t.join()
            i = i + n
            print('`', ','.join(stocks), '` download success')
            time.sleep(5)







if __name__ == '__main__':
    # 產生資料中心
    dc = DataCenter()
    # 輸出上市櫃證券代碼清單
    # print(dc.stocks)
    # 從證券代碼表來更新日線資料
    # dc.upgrade_daily_ohlcv_from_stocks()
    # 更新日線資料
    # dc.upgrade_daily_ohlcv('2317')
    # 將有問題的項目進行移除標示
    # dc.upgrade_mask_delisted()
    # print(dc.get_daily_ohlcv('2317'))
    # 
    # dc.upgrade_info('2317')
    # print(dc.get_info('2317'))
    # 
    dc.upgrade_info_from_stocks(50)