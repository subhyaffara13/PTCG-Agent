
def func2():
    class Test(trampoline_module.test_override_cache_helper):
        pass

    return Test()


def func2(*args, **kwargs):
    pass


def func2(a: str, b: int, c: float = 1.0) -> None:
    return None

