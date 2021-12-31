'''
【Python 的物件導向設計語法】

實體方法 Instance Method:
    無須修飾詞
    預設第一個參數為 self ，指向該類別(Class)的實體(Instance)。
    定義方式:
        def instance_method(self):
            pass

類別方法 Class Method:
    @classmethod 修飾詞
    預設第一個參數為 cls ，指向該類別(Class)。
    定義方式:
        @classmethod
        def class_method(cls):
            pass

靜態方法 Static Method:
    @staticmethod 修飾詞
    只當一般函式使用
    定義方式:
        @staticmethod
        def static_method():
            pass
'''


class Car:
    brand = ''
    type = ''
    cc = ''
    year = ''
    status = ''
    def __init__(self):
        pass
    # 靜態方法
    @staticmethod
    def static_info(who):
        print(f'品牌:{who.brand}, 車款:{who.type}, 排氣量:{who.cc}, 出廠年份:{who.year}, 車況:{who.status}')
    # 實體方法
    def info(self):
        Car.static_info(self)
    # 類別方法
    @classmethod
    def class_info(cls):
        Car.static_info(cls)

'''
【工廠模式 Factory Pattern】

設計模式(Design Pattern)之一，
工廠批量生產的設計概念，普遍運用在類別的生產。
若是要生產不同類別時，運用反射(Reflection)的方式來產生其實體。
'''
class CarFactory:
    # 靜態方法
    @staticmethod
    def create_car(brand, type, cc, year, status):
        import re
        regp_word = r'^[A-Z]{1}[a-z]+$'
        regp_str = r'^[A-Za-z \-]+$'
        regp_int = r'^[0-9]{4}$'
        regp_status = r'^[ABC]$'
        if not re.search(regp_word, brand):
            raise Exception('Error: brand')
        if not re.search(regp_str, type):
            raise Exception('Error: type')
        if not re.search(regp_int, str(cc)):
            raise Exception('Error: cc')
        if not re.search(regp_int, str(year)):
            raise Exception('Error: year')
        if not re.search(regp_status, status):
            raise Exception('Error: status')
        car = Car()
        car.brand = brand
        car.type = type
        car.cc = int(cc)
        car.year = int(year)
        car.status = status
        return car


car1 = Car()
car1.brand = 'Toyota'
car1.type = 'MVP'
car1.cc = 3000
car1.year = 2020
car1.status = 'A'
car1.info()
car1.class_info()

try:
    car1 = CarFactory()
except Exception as ex:
    print(ex)

car1 = CarFactory.create_car('Toyota', 'MVP', 3000, 2020, 'A')
try:
    car1 = CarFactory.create_car('toyota', 'MVP', 3000, 2020, 'A')
except Exception as ex:
    print(ex)
try:
    car1 = CarFactory.create_car('Toyota', '+MVP', 3000, 2020, 'A')
except Exception as ex:
    print(ex)
try:
    car1 = CarFactory.create_car('Toyota', 'MVP', '30.00+', 2020, 'A')
except Exception as ex:
    print(ex)
try:
    car1 = CarFactory.create_car('Toyota', 'MVP', 3000, -2000, 'A')
except Exception as ex:
    print(ex)
try:
    car1 = CarFactory.create_car('Toyota', 'MVP', 3000, 2020, 'Z')
except Exception as ex:
    print(ex)


car2 = CarFactory.create_car('Ford', 'Mondeo HyBird', 2000, 2020, 'A')
car2.static_info(car2)
Car.static_info(car2)