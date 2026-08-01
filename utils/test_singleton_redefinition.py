
def test_singleton_redefinition():
    class TestSingleton(Basic, metaclass=Singleton):
        pass

    assert TestSingleton() is S.TestSingleton

    class TestSingleton(Basic, metaclass=Singleton):
        pass

    assert TestSingleton() is S.TestSingleton

