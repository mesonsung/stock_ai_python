class FinalClass:

    def __init__(self, var):
        ## calling the set_a() method to set the value 'a' by checking certain conditions
        self.__set_a(var)

    ## getter method to get the properties using an object
    def __get_a(self):
        return self.__a

    ## setter method to change the value 'a' using an object
    def __set_a(self, var):

        ## condition to check whether var is suitable or not
        if var > 0 and var % 2 == 0:
            self.__a = var
        else:
            self.__a = 2

    a = property(__get_a, __set_a)

b = FinalClass(51)
b.a = 31
print (b.a)