
'''
執行緒也可以運用 OOP 來設計
好處是可以將分散的函式給組織化起來
同時建立不同用途的獨立工作者
'''

import random
import time
import threading



# 計時器
class Timer:
    __time = None
    def start(self):
        self.__time = time.time()
    def stop(self):
        if self.__time:
            return time.time() - self.__time
        return -1


# 工作日誌類別
class JobLog:
    # 工作權鎖
    __lock = threading.Lock()
    def write(self, msg):
        self.__lock.acquire()
        print(msg)
        self.__lock.release()


#工作類別
class Job:
    # 工作名稱
    name = ''
    # 工作日誌
    __log:JobLog = None
    # 工作完成事件
    __on_finish = None
    @property
    def on_finish(self):
        return self.__on_finish
    @on_finish.setter
    def on_finish(self, value):
        if callable(value):
            self.__on_finish = value
    # 初始化
    def __init__(self, name, log:JobLog, onfinish):
        self.name = name
        if type(log) == JobLog:
            self.__log = log
        if callable(onfinish):
            self.__on_finish = onfinish
    # 執行工作
    def do(self, **kwargs):
        if callable(self.__on_finish):
            sec = random.randint(1, 10)
            time.sleep(sec)
            kwargs['sec'] = sec
            self.__on_finish(**kwargs)
    # 工作回報
    def report(self, msg):
        if self.__log:
            self.__log.write(msg)


# 員工類別
class TEmployee(threading.Thread):
    # 工作任務
    __job:Job = None
    __kwargs = None
    # 建構式
    def __init__(self, job:Job, **kwargs):
        # 必須要讓父類別初始化
        threading.Thread.__init__(self)
        # 指派工作任務
        if type(job) == Job:
            self.__job = job
        # 指派工作任務參數
        self.__kwargs = kwargs
    # 覆寫(Override) Thread.run() 方法
    def run(self):
        if self.__job:
            ename = self.__kwargs['name']
            self.__job.report(f'{ename} 執行 `{self.__job.name}` 任務 ...')
            self.__job.do(name=ename, job=self.__job)


# 老闆類別
class Boss:
    # 員工集合
    __employees = list()
    # 工作清單
    __jobs = list()
    @property
    def jobs(self):
        return self.__jobs
    @jobs.setter
    def job(self, value):
        if type(value) == list:
            self.__jobs = value
    # 委派工作
    def invoke_job(self):
        for job in self.__jobs:
            ename = f'員工{len(self.__employees)+1}'
            job.report(f'委派 `{job.name}` 給 {ename}')
            employee = TEmployee(job, name=ename)
            self.__employees.append(employee)
            employee.start()
    # 等候
    def wait(self):
        for e in self.__employees:
            e.join()


# 任務完成事件處理程序
def job_on_finish(**kwargs):
    ename = kwargs['name']
    job = kwargs['job']
    sec = kwargs['sec']
    job.report(f'{ename} 任務 `{job.name}` 完成，耗時 {sec} 秒')


# 實體化計時器
timer = Timer()
# 實體化任務日誌
log = JobLog()
# 工作清單
jobs = ['蒐集資料', '彙整', '編輯報告書', '部務報告', '查看產線進度', '與設計部開會']

# 實體化老闆
boss = Boss()
# 進行工作清單彙整
for job in jobs:
    boss.jobs.append(Job(job, log, job_on_finish))
# 開始派發工作
log.write('馬克斯，開始委派任務')
boss.invoke_job()
log.write('馬克斯，委派任務結束')
# 等候所有工作完成
boss.wait()
print('--- end ---')