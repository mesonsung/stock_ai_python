
'''
函數 Function
    代表一項功能
    用於封裝(Encapsulation)邏輯程序
    具有輸入與輸出，也可視功能決定是否有輸入及輸出
'''

def random_walk(p, n):
    import random as rnd
    items = list()
    items.append(p)
    for i in range(n - 1):
        s = 1 if rnd.randint(0, 1) else -1
        p = p + rnd.randint(5, 10) * s
        items.append(p)
    return items

print(random_walk(100, 20))

'''
參數 *args
    表示傳入的參數都放入到 Tuple 的元組集合裡。

    傳入的參數具有順序性，務必要清楚每個順位的用途
        random_walk2(100, 20)

    直接傳入 Tuples 時，開頭須加上 *
        p = (100, 20)
        random_walk2(*p)
'''

def random_walk2(*args):
    p = args[0]
    n = args[1]
    import random as rnd
    items = list()
    items.append(p)
    for i in range(n - 1):
        s = 1 if rnd.randint(0, 1) else -1
        p = p + rnd.randint(5, 10) * s
        items.append(p)
    return items

print(random_walk2(100, 20))
params2 = 100, 20
print(random_walk2(*params2))


'''
參數 **kwargs
    **kwargs 表示傳入的參數都放入到 Dictionary 的字典集合裡。

    參數名稱可以用 key=value 指派，無須順序性
        random_walk3(n=20, p=100)

    若要傳入一個字典時，開頭須加上 **
        p = {'p':100, 'n':20}
        random_walk3(**p)
'''

def random_walk3(**kwargs):
    p = kwargs['p']
    n = kwargs['n']
    import random as rnd
    items = list()
    items.append(p)
    for i in range(n - 1):
        s = 1 if rnd.randint(0, 1) else -1
        p = p + rnd.randint(5, 10) * s
        items.append(p)
    return items

print(random_walk3(n=20, p=100))
params3 = { 'p':100, 'n':20 }
print(random_walk3(**params3))


'''
參數傳遞方式
    Pass by Value       將值複製後傳入，通常是：數值 Number, 布林 Boolean, 字元 Charactor
                        Python 則是 int, float, bool, str
    Pass By Reference   傳入記憶體位址共享
                        因為共享，所以會因指派而覆寫內容值
                        結構化記憶體因為其特性，都是傳入記憶體位址
                        Python 結構型態 list, dict, class
    Pass By Sharing     對於字典型態使用記憶體位址共享，有覆寫性
    Pass by Assignment  依指派的內容來決定 (Python 屬於這種)
'''


# 字串 String
a = '1111111'
def change(x):
    x[2] = 'X'
try:
    change(a)
except Exception as ex:
    print(ex)

# 串列集合 List
a = list('1111111')
change(a)
print(a)

# 唯一值集合 Set
a = {'1', '2', '3', '4', '5', '6', '7'}
try:
    change(a)
except Exception as ex:
    print(ex)

# 字典集合 Dictionary
a = {'1':'1', '2':'1', '3':'1', '4':'1', '5':'1', '6':'1', '7':'1'}
change(a)
print(a)


# 類別 Class
class Object:
    name = '1111111'

def change2(b):
    b.name = 'X'

a = Object()
change2(a)
print(a.name)
