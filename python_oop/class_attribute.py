'''
【Python 的物件導向設計語法】

屬性 Attribute:
    無須修飾詞。
    存取範圍，預設為公開(Public)。
    若限定於類別內部存取時，名稱字首用「__」兩個下底線標示。

邏輯屬性 Property:
    @property 修飾詞
        功能為「取值」。
        實作方式:
            @property
            def name(self):
                return self.__name

    @<propery 屬性>.setter 修飾詞
        功能為「賦值」。
        實作方式:
            @name.setter
            def name(self, value):
                if (type(value) == str):
                    self.__name = value
                else:
                    raise Exception(f'型態必須是 {type(str)}')

    @<propery 屬性>.deleter 修飾詞
        功能為「賦值」。
        使用須知:
            若該私有屬性是定義在 class 裡，是無法被刪除的。
            原因是 self 指向的是實體(Instance)記憶體，並非是定義類別(Class)記憶體。
        實作方式:
            @name.deleter
            def name(self):
                del self.__name
'''



class Student:
    id = ''
    __name = ''
    __age = 0

    def __init__(self):
        self.__sex = ''

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        if (type(value) == str):
            self.__name = value
        else:
            raise Exception(f'型態必須是 {type(str)}')

    @property
    def age(self):
        return self._age
    @age.setter
    def age(self, value):
        self._age = value
    @age.deleter
    def age(self):
        del self.__age
    
    @property
    def sex(self):
        return self.__sex
    @sex.setter
    def sex(self, value):
        self.__sex = value
    @sex.deleter
    def sex(self):
        del self.__sex



s1 = Student()
s1.id = '21001'
s1.name = 'Judy'

del s1.id
try:
    del s1.name
except Exception as ex:
    print(ex)

try:
    del s1.age
except Exception as ex:
    print(ex)
    print('因為是定義在 class 裡，所以無法刪除')

del s1.sex
try:
    print(s1.sex)
except Exception as ex:
    print(ex)
    print('因為是定義在 instance 裡，已經被刪除了')


exit()

