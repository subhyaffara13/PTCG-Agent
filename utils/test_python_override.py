
def test_python_override():
    def func():
        class Test(m.test_override_cache_helper):
            def func(self):
                return 42

        return Test()

    def func2():
        class Test(m.test_override_cache_helper):
            pass

        return Test()

    for _ in range(1500):
        assert m.test_override_cache(func()) == 42
        assert m.test_override_cache(func2()) == 0

