
'''
【通用應用程式記憶體組織架構概念】
Application 應用程式
    Heap  堆積區：
                    倉儲區概念。各類資料(變數、函式、類別等)定義存放的區域。
                    依全域(Global)與區域(Local)位置進行組織化管理。
    Stack 堆疊區：
                    用於執行函式的容器。
                    第一個執行函式為主程序 __main__。也就是應用程式的主要進入點的腳本檔案。
                    有先進後出的特性。　｜１｜２｜...｜６｜←　→　著名的河內塔原理。
                    執行數量有限額。很容易被設計不良的遞迴函式給塞爆。
    Queue 佇列區：
                    等待被回呼的函式。
                    有先進先出的特性。　←｜１｜２｜...｜６｜←　排隊原理。
                    來自於主執行緒與其他執行緒。


【通用記憶體存取概念】
Scope  範圍         屬於巢狀式架構，外層包著裡層，也是樹狀結構。
                        文件檔案屬於最外層(全域 Global)，樹狀的根節點(根 Root)。
                        流程控制、函式、類別是一層(區域 Local)，樹狀的子節點(Node 節點)。
                        函式內的子函式、類別內的方法、類別內的子類別等也是一層(區域 Local)，樹狀的子節點(Node 節點)。
                    Python 對於記憶體的存取僅限定於該層內(Scope 範圍)。
                        分別用 global 與 nonlocal 關鍵字來存取本層以外的記憶體。
                        算是它設計架構上的一種隔離保護機制，避免相同名稱的記憶體內容被複寫。
                        global 指的是使用根節點宣告的記憶體。
                        nonlocal 指的是使用上一層宣告的記憶體。
Global 全域         文件檔案本身。
                        宣告配置的記憶體隨著應用程式執行結束而消失
    Local 區域      流程控制、函式、函式內的函式、類別、類別方法。
                        宣告配置的記憶體隨著結構執行結束而消失。
'''


# Global
dog = 'global dog'

def local_dog():
    # Local
    dog = 'local dog'
    #
    def nonlocal_dog():
        # Local
        nonlocal dog
        dog = '> nonlocal dog'
        print(dog)
    #
    def global_dog():
        # Local
        global dog
        dog = '> global dog'
        print(dog)
    #
    print(dog)
    #
    nonlocal_dog()
    print(dog)
    #
    global_dog()
    print(dog)


print(dog)
local_dog()
print(dog)





'''
【結構化記憶體 Structure Memory】
基本上，每個儲存資料的記憶體都是單獨且分散的存在。
但是，有時候我們會需要將某些記憶體給串聯起來，方便管理取用。
就會使用一種連續型態的記憶體，稱之為陣列(Array)。
陣列的缺點，就是無法動態擴充。需要重新配置一個新的記憶體，複製完原資料後，再追加新元素進去。

因此，有了動態結構化記憶體(Dynamic Structure Memory)的設計概念，透過鏈結的方式，將分散的記憶體給鏈結起來。
鏈結的方式有：單向鏈結、雙向鏈結、樹狀鏈結、網狀鏈結等資料結構原理。
並依其資料結構的特性，設計存取值操作方法(先進先出、先進後出、遞迴探索)。
人工智慧的資料結構是採用類神經網路，也就是屬於網狀鏈結。
每個神經元，透過樹突(插座)與突觸(插頭)與其他神經元進行鏈結，形如網狀。

Python 的動態結構化記憶體
    串列 List           有序的元素集合。
    集合 Sets           無序且沒有重複的元素。
    字典 Dictionary     採用「鍵名 key」與「鍵值 value」來儲存元素，建名是具唯一性。
    元組 Tuples         不可以修改內容或增減其元素。
                        不支援append()、remove()、pop()等操作。
'''

class Student:
    pass

a = Student()
a.name = 'Judy'
a.sex = 'Female'
a.school = Student()
a.school.name = 'UCLA'
a.school.classroom = Student()
a.school.classroom.name = '3-A'
a.school.classroom.teacher = Student()
a.school.classroom.teacher.name = 'Mark'
a.school.classroom.teacher.sex = 'Male'
a.print = print
a.array = [1, 2, 3, 4, 5]
a.dicti = {'a':1, 'b':'Apple', 'c':True}


'''
遞迴 Recursion
    用於深度探索樹狀結構的一種演算法
    採用重複調用函式
    不適合用在網狀結構，會造成堆疊記憶體超量崩潰
'''

def recursion(x, node=''):
    for attr in x.__dict__:
        value = x.__dict__[attr]
        attr = attr if not node else f'{node}.{attr}'
        if type(value) is Student:
            print(f'{attr} is <Student>')
            recursion(value, attr)
        elif callable(value):
            print(f'{attr} is <Function>')
        else:
            print(f'{attr} = {value}')

recursion(a, 'a')
