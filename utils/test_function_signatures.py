
def test_function_signatures(doc):
    assert doc(m.test_callback3) == "test_callback3(arg0: Callable[[int], int]) -> str"
    assert doc(m.test_callback4) == "test_callback4() -> Callable[[int], int]"


def test_function_signatures(doc):
    assert doc(m.kw_func0) == "kw_func0(arg0: int, arg1: int) -> str"
    assert doc(m.kw_func1) == "kw_func1(x: int, y: int) -> str"
    assert doc(m.kw_func2) == "kw_func2(x: int = 100, y: int = 200) -> str"
    assert doc(m.kw_func3) == "kw_func3(data: str = 'Hello world!') -> None"
    assert doc(m.kw_func4) == "kw_func4(myList: List[int] = [13, 17]) -> str"
    assert doc(m.kw_func_udl) == "kw_func_udl(x: int, y: int = 300) -> str"
    assert doc(m.kw_func_udl_z) == "kw_func_udl_z(x: int, y: int = 0) -> str"
    assert doc(m.args_function) == "args_function(*args) -> tuple"
    assert (
        doc(m.args_kwargs_function) == "args_kwargs_function(*args, **kwargs) -> tuple"
    )
    assert (
        doc(m.KWClass.foo0)
        == "foo0(self: m.kwargs_and_defaults.KWClass, arg0: int, arg1: float) -> None"
    )
    assert (
        doc(m.KWClass.foo1)
        == "foo1(self: m.kwargs_and_defaults.KWClass, x: int, y: float) -> None"
    )

