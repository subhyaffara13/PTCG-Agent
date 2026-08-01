
def test_Singleton():

    class MySingleton(Basic, metaclass=Singleton):
        pass

    MySingleton() # force instantiation
    assert MySingleton() is not Basic()
    assert MySingleton() is MySingleton()
    assert S.MySingleton is MySingleton()

    class MySingleton_sub(MySingleton):
        pass

    MySingleton_sub()
    assert MySingleton_sub() is not MySingleton()
    assert MySingleton_sub() is MySingleton_sub()

