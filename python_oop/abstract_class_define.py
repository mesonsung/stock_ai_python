
'''
抽象 Abstract
    是指，有一種概念(可能是一種架構或是一種方法)其具體作法並不清楚，需要有人將它要怎麼做的方式給具體實作出來。
    不同人有不同的做法，但指向都是同一種概念。基於這些做法，有的會要求提供一些必要條件才能執行該做法。
    舉個例，有個概念「前往台北」，但沒有其具體作法。
    於是乎，有些人提出他們自己的具體作法。
        Ａ的具體作法：「雙腳走路」前往台北
        Ｂ的具體作法：「騎機車」前往台北
        Ｃ的具體作法：「開汽車」前往台北
        Ｄ的具體作法：「搭大眾運輸工具」前往台北
    以上，完成「前往台北」的具體作法裡，有的會要求必要條件：
        Ｂ：機車
        Ｃ：汽車
        Ｄ：大眾運輸工具
    若萬一符合上述條件的人，都可以選擇Ａ的作法
    
    基於一個概念衍伸多種形態與方法，OOP 稱為「多型(Polymorphism)」。
    基於類別的繼承(Inheritance)衍伸，再去做方法覆寫(Method Overriding)，也是多型的表現。

介面 Interface
    單純定義一些抽象方法，仍是需要套用的類別去實作具體程序。
    Python 類別的繼承方式是採用多個(非單一個)，因此可以用抽象類別做為實現介面的替代方式。
    介面在命名上，字首會用大寫 I 來表示。例如：IRecordControl 紀錄控制介面
'''




'''
ABC: 抽象基礎類別(Abstract Base Class, ABC)
    透過匯入 abc 模組，可參考下列項目：

        抽象基礎類別，透過繼承 ABC 類別，或是繼承時指定 metaclass=ABCMeta
            ABC 是基於 ABCMeta，是為了讓類別可以直接繼承
                class A(ABC):
                    pass
            或
                class A(metaclass=ABCMeta):
                    pass

        抽象邏輯屬性(Abstract Property)，使用 @abstractproperty 修飾詞(Decorator)
            3.3 版已移除，改用 @property 搭配 @abstractmethod
                @property
                @abstractmethod
                def name(self):
                    pass

                @name.setter
                @abstractmethod
                def name(self, value):
                    pass

        抽象方法(Abstract Method)，使用 @abstractmethod 修飾詞(Decorator)
            抽象方法，第一個參數值指向的是類別經過實體化後的記憶體 self
            @abstractmethod
            def go(self, param1):
                pass

        抽象類別方法(Abstract Method)，使用 @abstractclassmethod 修飾詞(Decorator)
            與抽象方法的差別，在於第一個參數值指向的是 class 定義的記憶體 cls，
            不是指向已經實體化的記憶體 self。因此，在存取上要特別留意。
            @abstractclassmethod
            def go(cls, param1):
                pass

        抽象靜態方法(Abstract Method)，使用 @abstractstaticmethod 修飾詞(Decorator)
            r
            @abstractstaticmethod
            def build(param1, param2, param3):
                pass
'''
from abc import \
    ABC, \
    ABCMeta, \
    abstractmethod, \
    abstractclassmethod, \
    abstractstaticmethod


'''
抽象類別(Abstract Class)
定義一個概念結構與需求方法，但不會去考慮它具體怎麼做
'''
class BaseLogin(ABC):
    @abstractmethod
    def login(self):
        pass

'''
實作抽象類別(Implementation Abatract Class)
基於一個抽象概念，去實作它的具體作法
'''
class UserLogin(BaseLogin):
    def login(self):
        print('User login')

'''
有的會要求提供必要條件
'''
class ManagerLogin(BaseLogin):
    def login(self, account, password):
        if (account == 'admin' and password == 'admin'):
            print('Manager login')
        else:
            print('Verify fail')

try:
    print('抽象類別，進行實體化 ...')
    bl = BaseLogin()
    bl.login()
except Exception as ex:
    print(ex)
    print('抽象類別 BaseLogin 無法實體化')

print('實作抽象類別的具體作法類別，進行實體化 ...')
ul = UserLogin()
ul.login()

print('實作抽象類別的具體作法類別，進行實體化 ...')
ml = ManagerLogin()
ml.login('user', 'user')
ml.login('admin', 'admin')


'''
介面實作
'''

class IRecordControl(ABC):
    @abstractstaticmethod
    def create():
        pass
    @abstractstaticmethod
    def read():
        pass
    @abstractstaticmethod
    def update():
        pass
    @abstractstaticmethod
    def delete():
        pass
    
class IRecordQuery(ABC):
    @abstractmethod
    def query():
        pass
    @abstractclassmethod
    def execute():
        pass

class MySQL(IRecordControl, IRecordQuery):
    pass

class MSSQL(IRecordControl, IRecordQuery):
    __intro = ''
    def __init__(self):
        self.__intro = 'Microsoft SQL Server'
    @property
    def intro_from_instance(self):
        return self.__intro
    @classmethod
    def intro_from_class(cls):
        return cls.__intro

    def create():
        print('MSQL :: create 抽象靜態方法實作')
    def read():
        print('MSQL :: read 抽象靜態方法實作')
    def update():
        print('MSQL :: update 抽象靜態方法實作')
    def delete():
        print('MSQL :: delete 抽象靜態方法實作')
    def query(self):
        print(f'MSQL :: query 抽象方法 `{self.intro_from_instance}`')
    def execute(cls):
        print(f'MSQL :: execute 抽象類別方法 `{cls.intro_from_class()}`')


MySQL.create()
MySQL.read()
MySQL.update()
MySQL.delete()
MySQL.query()
try:
    MySQL.execute()
except Exception as ex:
    print(ex)
    print('因為是抽象類別方法，必須有第一個參數 cls')
try:
    mysql = MySQL()
except Exception as ex:
    print(ex)
    print('因為沒有實作任何抽象方法的具體程序，等同於抽象類別，無法進行實體化')




MSSQL.create()
MSSQL.read()
MSSQL.update()
MSSQL.delete()
try:
    MSSQL.query()
except Exception as ex:
    print(ex)
    print('因為是抽象方法實作，必須有第一個參數 self')

mssql = MSSQL()
try:
    mssql.create()
except Exception as ex:
    print(ex)
    print('因為是實體物件，實作方法時，必須定義第一個參數 self')
mssql.query()
mssql.execute()

