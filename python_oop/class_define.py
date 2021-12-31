'''
物件導向設計 Object Oriented Programming, OOP
    基於生物世界的概念，從基因特徵的定義、物種的多樣性、物種的繁殖、到生物之間的互動，達到一個仿生的程式設計架構。
    生物本身都是被動(Passive)的，不會主動(Active)去做任何事，都是透過事件來驅動牠去做出反應，我們稱之為「事件驅動 Event Driven」。
    像是「吃」這個動作，是基於生理被刺激(看到美食，聞到香味、肚子發出咕咕聲)反應之後，才決定做出的動作。
    如果還不能理解，網頁瀏覽器它不會主動去執行開啟，需要我們去執行它，這時它才會執行開啟程序。
    等到開啟完成後，又回復到被動狀態，等待使用者對它進行操作。

類別 Class
    可以將它當成是一個基因(DNA)、模具(Mold)或是設計圖(Design diagram)，透過繁殖(Reproduce)、生產(Create)或建置(Build)的方式產生出實體。
    實體(Instance)，又可稱為物件(Object)，對應用程式來說是一種結構化的記憶體。
    類別具有下列的結構性特徵：
        繼承 Inheritance        : 類似於配種(Breeding)，可以衍生出很多代，是一種多型(Polymorphism)的表現。
                                : 多數的 OOP 程式語言限定類別僅能繼承於單一類別。
        屬性 Attribute          : 用來供外界辨識的特徵，以分辨出屬於哪一類物種。
            欄位屬性 Attribute  : 類似於儲存格(變數)，具有取值與賦值的特性。
            邏輯屬性 Property   : 是一種邏輯方法(函式)，當欄位屬性要取值或賦值之前，都得必須經過一套程序才能進行取值或賦值的動作。
        方法 Method             : 是可以完成某種任務的功能(函式)。
            覆寫 Override       : 子類別(Child Class)覆寫父類別(Parent Class)原生方法(Native Method)的一種做法。
            多載 Overload       : 子類別覆寫父類別原生方法，並提供多樣性輸入條件(參數 Parameter)的一種做法。
            靜態 Static         : 無須透過類別實體化才能存取的方法。
                                : 直接用類別就可以調用該方法。 <類別>.<方法>() 特性跟模組內的函式一樣。
                                : 所以，靜態方法對 OOP 來說，是將可以直接調用的函式給予組織化。
        事件 Event              : 用來偵測實體的屬性發生異動或是執行某個方法之後，用來觸發對應的反應動作。
                                : 也是因為觸發反應動作，所以產生了互動(Interactive)。
                                : 這就是物件導向設計裡最擬人化的一刻。
                                : 基本上，是以一個預設值為 Null 無值(Python 是 None)的屬性，又稱為事件屬性。
                                : 由設計者，實體化類別後，再去將定義好的函式(反應程序)指派它即可(物件.事件屬性 <= 函式)。
                                : 之後，由類別預先定義好的「約束屬性或方法」內去觸發執行它。
        事件訊息 Event Message  : 觸發反應動作時，傳入的訊息。也就是函式的傳入參數(Parameter)。

抽象類別 Abstract
    基於一種概念化(有想法卻沒具體作法)的類別。
    初步定義好一些架構，但其中的方法只有定義其名稱與傳入參數，但具體做法卻沒有定義，稱之為「抽象方法(Abstract Method)」。
    必須得透過繼承衍生的方式，由子代來實作(Implement)其抽象方法(Abstract Method)的具體實現程序。
    也因為如此，不同的子代其具體作法有異，造就了多樣性，我們稱之為：多型(Polymorphism)。

介面 Interface
    類似於抽象類別，卻沒有架構，只有抽象方法。
    強制去約束套用該介面的類別必須要去實作其定義之抽象方法與具體實現程序(可以略過具體實現程序)。
    特性是一個介面可以讓多個類別去套用它。
    可以理解成設計規格書，書內定義必須要有哪些規格(抽象方法)，但沒要求具體做法(具體實現程序)。
    例如：Gogoro 電池座規格介面。所有欲使用該電池的電動機車廠商都必須依規格製作。
    至於外型、材質、擺放位置等細節沒有要求，只要有按電池座規格(約束)可安裝該電池並正常供電即可。

強型 Strong
    是指變數僅能儲存指定型態的資料。
    編譯式程式語言(C, C++, Java, C#, VB.Net)採用的是強型程式設計架構。
    會強制要求宣告變數時，必須得指定其內容為何種資料型態。
    宣告完成之後，當指派資料給該變數時，就會檢查是否符合其宣告型態。
    發現不符合時就擲出「型態指派錯誤」。
    像是單晶片韌體程式設計，在擴充的記憶體需要自行管理時，
    強型的優點就會凸顯出來，以利掌握有限的記憶體空間。

泛型 Generic
    是指變數可以儲存任何一種資料型態。
    直譯式程式語言(JavaScript, PHP, Python)是採用泛型程式設計架構，
    也就是變數的資料型態就是泛型。
    泛型的優點也是缺點，因為不知道其內容是什麼型態，經常會被亂存，也因此要檢查資料型態後才能決定怎麼用。
    否則，經常會報錯，有的公司會要求程式碼撰寫規範上，變數名稱命名上使用<型態簡寫><名稱>，例如：intMoney，整數型別的 Money 變數。
    Python 在 3.5 版本之後，有了「typing 型態標示」的語法糖，但僅限於標示作用。
    例如:
        a1:int = 10
        b1:int = 20
        def sum(a:int, b:int) -> int:
            return a + b
        c:int = sum(a1 + b1)


物件導向設計，源起於 C++ ，之後被 Java 廣泛應用。
可以完全實作於編譯式的程式語言，而直譯式的程式語言只是運用語法糖(Syntax candy)方式去部分實作。
Python 對於 OOP 在 2.4 版本以後，透過新功能「修飾詞 Decorator」 @ 符號，幾乎可以實作出來。
'''





'''
【Python 的物件導向設計語法】

類別定義，命名上規範單字字首為大寫，如 Animal、DockDun。

    class <類別名稱>:
        pass


實體化，如同執行函式一樣。

    <變數:物件> = <類別>()


實體化方法，俗稱建構式(Constructor / Initionalize)。
定義類別進行實體化時必須要執行的程序。
內定參數為 self 表示該類別的實體，進而可以存取其內部定義的項目。
例如 self.name = 'Animal' 將 'Animal' 字串指派給屬性 name。

    def __init__(self):
        pass
'''

# 類別定義
from typing import Callable


class Animal:
    name = '動物'
    def __init__(self):
        pass
    def intro(self):
        print(f'我是 {self.name}')
    def say(self):
        print(f'{self.name}: ...')

# 類別實體化與操作
a = Animal()
a.intro()
a.say()




'''
【Python 的物件導向設計語法】

類別繼承
    繼承某個類別，產生子代。
    Python 不限於單一繼承，可多重繼承。
    繼承的子代，除了繼承原生架構，亦可以覆寫父代的原生方法
    同時，也可以追加屬於自己的架構。
    要使用父代時，可用 super() 函是來取得父代實體進行操作

    class <類別名稱>(<繼承的類別>, ...):
        def __init__(self):
            # 執行父代的實體化程序
            super().__init__()
'''


# 類別定義
class Dog(Animal):
    def __init__(self):
        super().__init__()
        self.name = '狗'
    def say(self):
        print(f'{self.name}: 汪汪汪')

class Cat(Animal):
    def __init__(self):
        super().__init__()
        self.name = '貓'
    def say(self):
        print(f'{self.name}: 喵~')

# 類別實體化與操作
dog = Dog()
dog.intro()
dog.say()

cat = Cat()
cat.intro()
cat.say()



'''
【Python 的物件導向設計語法】

存取範圍 Access Scopt
    用於定義「屬性、方法與事件」的存取條件，預設是公開(Public)。
    若要限定為 Class 內部才能存取，透過字首開頭以 __ 兩個底線的命名方式限定為私有(Private)。
        例如：私有屬性 __name 或私有方法 def __go(self, target):
    
    僅是在「讀取或執行」的情況下，遇到「私有」時才會受到限制。
    若是在「指派(存入)」的情況下，基於泛型(Generic)設計原則，
    是可以在實體下動態串聯新的屬性，但是卻會覆寫到類別原生的同名屬性。
    原生的 <class 'Dock'>.__is_hungry 記憶體位址被取代為新的 __is_hungry 的記憶體位址
        例如：dock.__is_hungry = True
'''

# 類別定義
class Dock(Animal):
    __is_hungry = False
    def __init__(self):
        super().__init__()
        self.name = '鴨子'
    def __hungry(self):
        print(f'{self.name} 現在肚子餓了')
    def now(self):
        import random
        self.__is_hungry = False if random.randint(0, 1) else True
        if self.__is_hungry:
            self.__hungry()

# 類別實體化與操作
dock = Dock()
dock.intro()
dock.say()
dock.now()
try:
    print(dock.__is_hungry)
except Exception as ex:
    print(f'Error: {ex}')
try:
    dock.__hungry()
except Exception as ex:
    print(f'Error: {ex}')

# 將 __is_hungry 動態鏈結到 dock 記憶體
dock.__is_hungry = True
print(f'串聯後，dock.__is_hungry: {dock.__is_hungry}')
dock.now()


'''
【Python 的物件導向設計語法】

@property 修飾詞
    讓類別屬性(Attribute)可以具有像函式般，對私有屬性進行邏輯性的存取
    使用上仍是像指派(Assign)一樣 student.name = 'John'

    @property                       邏輯屬性::取值
    def 函式名稱(self):
        return self.__私有屬性

    @<函式名稱>.setter              邏輯屬性::存值
    def 函式名稱(self, value):
        self.__私有屬性 = value
'''

# 類別定義
class Actor:
    # 私有::欄位屬性 ---------------------------
    __base = ''
    __name = ''
    __hp = 0
    __power = 0
    __on_attack = None
    __on_die = None
    # 實體化建構式
    def __init__(self, base):
        self.__base = base
    # 公開::邏輯屬性 ---------------------------
    @property
    def name(self):
        return f'{self.__name}({self.__base})'
    @name.setter
    def name(self, value):
        self.__name = value
    @property
    def hp(self):
        return self.__hp
    @hp.setter
    def hp(self, value):
        if value > 0:
            self.__hp = value
        else:
            self.__hp = 0
            self.die()
    @property
    def power(self):
        return self.__power
    @power.setter
    def power(self, value):
        self.__power = value
    # 公開::事件屬性 ---------------------------
    @property
    def on_attack(self):
        return self.__on_attack
    @on_attack.setter
    def on_attack(self, event_func):
        if callable(event_func):
            self.__on_attack = event_func
    @property
    def on_die(self):
        return self.__on_die
    @on_die.setter
    def on_die(self, event_func):
        if callable(event_func):
            self.__on_die = event_func
    # 公開::方法 ---------------------------------
    def attack(self, target):
        print(f'{self.name} 力量 {self.power} ，攻擊 {target.name}')
        target.hp = target.hp - self.power
        if target.hp > 0:
            print(f'{target.name} 生命值剩下 {target.hp}')
            if callable(target.on_attack):
                target.on_attack(self)

    def die(self):
        print(f'{self.name} 被消滅了')
        if callable(self.on_die):
            self.on_die(self)


class Boss(Actor):
    def __init__(self):
        super().__init__('魔王')
        self.hp = 10000
        self.power = 200


class Hero(Actor):
    def __init__(self):
        super().__init__('英雄')
        self.hp = 1000
        self.power = 50



# 類別實體化與操作
hero = Hero()
hero.name = '瑪莉大哥'
print(f'{hero.name} 已產生')

boss = Boss()
boss.name = '庫巴'
print(f'{boss.name} 已產生')

print(f'讓 {hero.name} 發起攻擊，目標是 {boss.name}')
hero.attack(boss)


'''
【Python 的物件導向設計語法】

透過觸發事件來進行互動。
原理實作：
    定義好某個事件回應的處理函式，再指派給實體的事件屬性。
    之後，只要該實體的事件被觸發後，就會執行事件回應的處理函式。
'''

def hero_on_attack(who):
    hero.attack(who)
    # if hero.hp > 300:
    #     hero.attack(who)
    # else:
    #     print(f'{hero.name} 逃跑了')
hero.on_attack = hero_on_attack

def boss_on_attack(who): 
    boss.attack(who)
boss.on_attack = boss_on_attack

def actor_on_die(who):
    print(f'{who.name} has dead!')

hero.on_die = actor_on_die
boss.on_die = actor_on_die

print(f'讓 {boss.name} 發起攻擊，目標是 {hero.name}')
boss.attack(hero)

