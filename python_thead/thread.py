
'''
行程 Process 與 執行緒 Thread

【運作原理】
    先來談處理器(CPU)怎麼做到多工？
    簡單說，在多個行程(Process)間快速切換執行，快到讓人類感覺不出來就可以了。
    CPU 的規格 1.2GHz 指的是，每秒可以處理的指令數量可達 1.2G (1,200,000,000 cmd/sec)個指令。
    總結，每個行程都輪流做一點，因為太快了，感覺像是每個行程都在執行。

    由作業系統配發的一個行程(Process)派令，給要求執行的應用程式(Application)。
        行程本身有五個狀態：
            產生(New)       ：行程產生中。
            就緒(Ready)     ：行程準備好了並放入到程序池(Process pool)內，等候處理器(CPU)來執行。
            執行(Running)   ：行程正在被處理器執行指令中。
            等待(Waiting)   ：處理器執行指令過程中發生某些事(I/O、事件、網路通訊)，導致處理器暫停執行，也就是形成等待狀態。
            結束(Terminated)：行程執行結束，從程序池內移除。
        過程中，行程的狀態會處於
            產生 → 就緒 → 執行 → 等待 → 就緒 → 執行 → 等待 ...結束
    
    行程會產生一個主執行緒(Main thread)，來執行應用程式的主要程序 main() 函式。
        主執行緒的堆疊(Stack) <- main()
    
    若過程中，有部分的程序執行時間過久或不確定時，會造成阻塞(Blocking)現象，導致無法繼續往下執行。
    要解決這個問題，可以產生一個子執行緒(Sub thred)，然後將該程序封裝成函式 sub() 後，交派給子執行緒來執行。
        子執行緒的堆疊(Stack) <- sub()
    這樣一來，就不會影響主執行緒的工作。

    架構
        行程(Process)               => 應用程式(Application)
            主執行緒(Main thread)   => 主程序 main()
            子執行緒(Sub thread)    => 函式 f()
    
    乍看之下，執行緒本身就像是一個獨立工作者，然後完成自身交派的工作任務。
    執行緒的特性：
        隔離封閉：也就是彼此間互不干擾對方的工作。
        通訊委派：若要傳達訊息給另一個執行緒，就必須透過委派(Invoke)來傳遞。
    解決執行緒間的通訊方法
        訊息佇列：佇列(Queue)有著先進先出的特性，可以將外部訊息放入其中等候來處理。
    
    行程(Process)本身除了主執行緒(Main thread)外，還有其它的子執行緒(Sub thred)要管理，
    若任何一個執行緒尚未執行完成，行程是不會結束的。
    所以應用程式本身也需要運用程序池的管理機制，來做執行緒的管理。
    以確保，不會造成濫用執行緒，以及監控執行緒是否有失控情況。


【擬人化概念一】
    可以想像成是一個上班族 (應用程式)。
    上班打卡後 (行程準備就緒，已放入程序池內等候處理器來執行)，
    開始今天的工作 (產生一個主執行緒，執行 main() 主程序)，
    直到下班打卡為止 (行程執行結束，從程序池內移除)。

    模擬阻塞
        中午外出吃飯 (執行函式)，
        結果大排長龍，吃飯時間變長了 (行程阻塞)，
        導致工作時間被迫也延長了，無法下班 (超過預期的執行時間)。

    阻塞的解決方案
        交派給粉紅熊貓買午餐 (產生子執行緒，交派任務執行)。
        工作到一個段落，查看有無送來 (查看訊息佇列)。
            沒有，繼續工作
            有，暫停工作，去吃飯

【擬人化概念二】
    有個專案計畫 (應用程式)。
    已經通過預算審核並啟動 (行程準備就緒，已放入程序池內等候處理器來執行)，
    由專案經理全權負責 (主執行緒)，
    過程，有很多個子任務要執行，若全由專案經理獨自負責，肯定會無法在期限內完成。
    因此，就將子任務分派給子任務負責人去執行 (產生子執行緒，並交派欲執行的程序)，
    過程，專案經理可以隨時透過任務進度表來掌握行程 (執行緒池)。
    過程，任務負責人隨時透過「代辦事項表與任務回報表」跟專案經理與子任務負責人進行通訊 (訊息佇列)。
    最終，所有子任務均順利完成，專案經理也已經可以正式結束專案計畫 (行程執行結束，從程序池內移除)。
    萬一，計畫執行期間遇到強制中止時，專案經理可以透過通訊告知子任務負責人立即中止 (執行緒中止旗標)。
'''



'''
只有主執行緒在執行
    模擬當一個人要獨自完成所有耗時工作
'''

import time
import random

# 計時器
class Timer:
    __time = None
    def start(self):
        self.__time = time.time()
    def stop(self):
        if self.__time:
            return time.time() - self.__time
        return -1

# 實體化計時器
timer = Timer()


# 列印標題
def print_title(title):
    # 是否為全形字
    def is_full_char(uchar):
        i = ord(uchar)
        return i > 126
    # 取字串長度
    def get_len(string):
        n = 0
        for c in list(string):
            # print(c, ord(c), is_full_char(c))
            n = n + (1,2)[is_full_char(c)]
        return n
    # 產生線段並輸出
    line = '-' * get_len(title)
    print(f'{line}\n{title}\n{line}')




# 參數
actor = '馬斯克'
items = ['蒐集資料', '彙整', '編輯報告書', '部務報告', '查看產線進度', '與設計部開會']
rnd_s = 3
rnd_e = 10

# 獨自一人
def alone():
    global items
    print(f'{actor} 一天工作開始')
    # 計時開始
    timer.start()
    t_sec = 0
    for i in range(len(items)):
        t_sec = t_sec + do_something(items[i])
    # 計時結束
    sec = timer.stop()
    print(f'{actor} 一天工作結束，共耗費 {sec} 秒 > 總工時 {t_sec} 秒')

# 做工作
def do_something(name):
    print(f'{actor} 執行 {name} 中 ....')
    sec = random.randint(rnd_s, rnd_e)
    time.sleep(sec)
    print(f'{actor} 執行 {name} 完成，耗費 {sec} 秒')
    return sec

# 執行
# print_title('一個人獨自完成所有任務')
# alone()






'''
Python 多執行緒
    threading 模組內的 Thread 類別
        t = threading.Thread(
            name=<名稱>,
            target=<處理函式>,
            args=(<函式的參數>, ...)
        )
        t.join()        等待，會形成阻塞(Blocking)狀態，直到該執行緒執行完程序，呈現「就緒」狀態
        t.isAlive()     是否在執行狀態?
'''

'''
主執行緒交派任務給子執行緒
    模擬當一個人，可以交派工作給其他人立即去執行
    個別管理這些任務負責人
    等候方式
        1. 不用等候，結束主任務程序
        2. 等候該任務負責人完成後，再交派下個任務給負責人。直到最終任務完成，才結束主任務程序
'''

import threading

# 多個執行緒
def invoke_job_and_run_now(wait=False):
    global items
    print(f'{actor} 一天工作開始')
    # 計時開始
    timer.start()
    print("交派任務中 ...")
    for i in range(len(items)):
        print(f'分派任務 `{items[i]}` 給負責人{i+1}')
        t = threading.Thread(
            target=do_invoke,
            args=(items[i], i+1)
        )
        t.start()
        if wait: t.join()
    print("交派任務完成")
    # 計時結束
    sec = timer.stop()
    print(f'{actor} 一天工作結束，共耗費 {sec} 秒')

# 交派工作
def do_invoke(name, no):
    global message_queue
    print(f'任務負責人{no} 執行 `{name}` 中 ....')
    sec = random.randint(rnd_s, rnd_e)
    time.sleep(sec)
    print(f'任務負責人{no} 執行 `{name}` 完成，耗費 {sec} 秒')

# 執行
# print_title('交派任務::交派完，立即去處理。無須等候任務負責人，結束一天的行程')
# invoke_job_and_run_now()


# 執行
# print_title('交派任務::交派完，立即去處理，並等候該任務完成後，再交派下個任務。直到完成最終任務，結束一天的行程')
# invoke_job_and_run_now(True)


'''
主執行緒交派任務給子執行緒
    模擬當一個人，可以交派工作給其他人去執行
    集中管理這些任務負責人，並決定他們執行任務的方式
        1. 接獲任務，立即執行
        2. 接獲任務，再集體執行（假的！仍是逐筆執行，因為速度很快所以感覺像是集體）
    都必須等候任務全數完成後，才結束主任務程序
'''

# 執行緒池
pool = list()

# 委派任務並集體行動
# run_together: 是否要集體行動?
def invoke_job_and_run_together(run_together=False):
    global items, pool
    print(f'{actor} 一天工作開始')
    # 計時開始
    timer.start()
    print("交派任務中 ...")
    for i in range(len(items)):
        print(f'分派任務 `{items[i]}` 給負責人{i+1}')
        t = threading.Thread(
            target=do_invoke,
            args=(items[i], i+1)
        )
        pool.append(t)
        if not run_together: t.start()
    print("交派任務完成")
    # 是否要集體行動?
    if run_together:
        for t in pool:
            t.start()
    # 等候
    for t in pool:
        t.join()
    # 計時結束
    sec = timer.stop()
    print(f'{actor} 一天工作結束，共耗費 {sec} 秒')


# 執行
# print_title('交派任務::交派完後，立即執行。等候最後完成任務的負責人，在結束一天的行程')
# invoke_job_and_run_together()

# 執行
# print_title('交派任務::先交派完後，再一起執行。等候最後完成任務的負責人，在結束一天的行程')
# invoke_job_and_run_together(True)



'''
模擬各個任務負責人要回報執行進度
    執行進度要寫入到日誌 (用終端機I/O來取代日誌)
'''

# 執行緒池
pool = list()
# 訊息佇列
message_queue = list()
# 結束旗標
is_end = False

# 任務回報
# use_queue: 是否使用訊息佇列?
def job_report(use_queue=False):
    print(f'{actor} 一天工作開始')
    global is_end
    # 結束旗標設為關閉
    is_end = False
    # 計時開始
    timer.start()
    do_output(f'交派任務中 ...', use_queue)
    # 啟動訊息佇列列印器
    t_name = f'T-Msg-Printer'
    t = threading.Thread(
        name=t_name,
        target=print_message_queue
    )
    t.start()
    # 分派任務
    for i in range(len(items)):
        t_name = f'T-{i+1}'
        t = threading.Thread(
            name=t_name,
            target=do_report,
            args=(items[i], i+1, use_queue)
        )
        pool.append(t)
        do_output(f'分派任務 `{items[i]}` 給負責人{i+1}，任務編號:{t_name}，收到後立即去執行', use_queue)
        t.start()
    do_output(f'交派任務完成', use_queue)
    # 等候任務
    for t in pool:
        alive = ('就緒', '執行')[t.isAlive()]
        do_output(f'>>>> {t.name} {alive}', use_queue)
        t.join()
        alive = ('就緒', '執行')[t.isAlive()]
        do_output(f'>>>> {t.name} {alive}', use_queue)
    # 計時結束
    sec = timer.stop()
    do_output(f'{actor} 一天工作結束，共耗費 {sec} 秒', use_queue)
    # 結束旗標設為啟動
    is_end = True

# 輸出訊息
# msg: 訊息
# use_queue: 是否使用訊息佇列?
def do_output(msg, use_queue):
    if not use_queue:
        print(msg)
    else:
        message_queue.append(msg)

# 執行回報
# job: 任務
# no: 負責人
# use_queue: 是否使用訊息佇列?
def do_report(job, no, use_queue):
    do_output(f'任務負責人{no} 任務 `{job}` 開始執行', use_queue)
    n = random.randint(1, 5)
    for i in range(n):
        time.sleep(random.randint(3, 10))
        do_output(f'任務負責人{no} 回報任務 `{job}` 仍在進行中 >>> 次數 {i+1}/{n}', use_queue)
    do_output(f'任務負責人{no} 任務 `{job}` 已完成', use_queue)

# 列印訊息佇列
def print_message_queue():
    while True:
        if len(message_queue) > 0:
            print(message_queue.pop(0))
        if is_end and len(message_queue) < 1: return

# 執行
# print_title('交派任務::交派完隨即執行，但必須要做進度回報。回報者直接去寫入日誌')
# job_report()

'''
改良日誌被大家寫得亂七八糟
'''

# 執行
# print_title('交派任務::交派完隨即執行，但必須要做進度回報。將回報訊息放入到訊息佇列裡，由訊息列印器負責寫日誌')
# job_report(True)




'''
執行緒鎖 Thread Lock

    前言
        執行緒的特性與工作方式，透過案例我們可以發現一件事，「共用資料存取(Common Data Access)」的問題。
        像是：輸出入(Input/Output, I/O)、網路通訊這類必須會用到的緩衝區串流(Buffer Stream)，也是記憶體。
        若很多執行緒在寫入資料時，因個別的資料長度不等，相對在資料寫入的過程時，就會被插隊，導致資料無法連貫。
        
        為何會有插隊的問題？還記得處理器(CPU)是如何達到多工作業！這也就是造成插隊的主因。
        處理器不可能為了一個耗時很久的程序指令(迴圈, I/O, 通訊)去影響多工作業。
        
        也因此，我們會運用佇列原理來處理。但是，別忘了！再怎麼樣都是同一個用途的記憶體。
        短資料的寫入還尚可，但長資料呢？「資料共用」的問題仍是存在！

    需求
        我們希望當共用同一個用途的記憶體時，正在使用的人可以完整的寫完資料（包含檢查資料的完整性）後，再輪到下個人去寫。
        也就是進入檔案室後將門上鎖，直到使用完後，才將門解鎖。

    方案
        鎖(Lock)的原理大家都明白，利用鎖的特性：「上鎖與解鎖」就可以去解決執行緒間的共用資料的插隊問題。
        當某個執行緒要執行「共用資料存取」程序前，先行「上鎖 Lock」。直到完成「共用資料存取」後，再行「解鎖 Unlock」。

    Python
        1. 透過 threading 模組內的 Lock 類別，實體化產生一個鎖 lock。
            lock = threading.Lock()
        2. 用鎖的 acquire() 方法，將目前行程內的工作權鎖定給要求的執行緒，其它執行緒就處於等待。
            lock.acquire()
        3. 直到該執行緒處理完後，就用鎖的 release() 方法，將目前行程內的工作權給釋出。
            lock.release()
        可以透過 locked() 去查看哪個執行緒處於鎖定狀態。
'''


# 實體化執行緒鎖
lock = threading.Lock()
# 執行緒池
pool = list()


# 任務鎖定作業
# use_lock: 是否要使用工作權鎖?
def job_lock(use_lock=False):
    print_lock(f'{actor} 一天工作開始', use_lock)
    # 計時開始
    timer.start()
    print_lock(f'交派任務中 ...', use_lock)
    # 分派任務
    for i in range(len(items)):
        t_name = f'T-{i+1}'
        t = threading.Thread(
            name=t_name,
            target=do_common_data_access,
            args=(items[i], i+1, use_lock)
        )
        pool.append(t)
        print_lock(f'分派任務 `{items[i]}` 給負責人{i+1}，任務編號:{t_name}，收到後立即去執行', use_lock)
        t.start()
    print_lock(f'交派任務完成', use_lock)
    # 等候
    for t in pool:
        t.join()
    # 計時結束
    sec = timer.stop()
    print_lock(f'{actor} 一天工作結束，共耗費 {sec} 秒', use_lock)


# 共用資料存取
# job: 任務
# no: 負責人
# use_lock: 是否要使用工作權鎖?
def do_common_data_access(job, no, use_lock):
    print_lock(f'任務負責人{no} 工作權 > 上鎖', use_lock)
    n = random.randint(0, 5)
    sec = random.randint(1, 10)
    for i in range(n):
        print_lock(f'任務負責人{no} 回報任務 `{job}` >>> {i+1}/{n}', use_lock)
        time.sleep(sec)
    print_lock(f'任務負責人{no} 工作權 > 解鎖，耗時 {sec} 秒', use_lock)


# 輸出到終端機採用工作權鎖
# msg: 訊息
# use_lock: 是否要使用工作權鎖?
def print_lock(msg, use_lock):
    if use_lock:
        lock.acquire()
        print(msg)
        time.sleep(0.3)
        lock.release()
    else:
        print(msg)


# 執行
# print_title('交派任務::交派完隨即執行，但必須要做進度回報。回報者可以插隊去寫入日誌')
# job_lock()


# 執行
print_title('交派任務::交派完隨即執行，但必須要做進度回報。回報者必須要使用工作權鎖去寫入日誌')
job_lock(True)


