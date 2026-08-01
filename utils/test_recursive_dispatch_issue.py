
def test_recursive_dispatch_issue():
    """#3357: Recursive dispatch fails to find python function override"""

    class Data(m.Data):
        def __init__(self, value):
            super().__init__()
            self.value = value

    class Adder(m.Adder):
        def __call__(self, first, second, visitor):
            # lambda is a workaround, which adds extra frame to the
            # current CPython thread. Removing lambda reveals the bug
            # [https://github.com/pybind/pybind11/issues/3357]
            (lambda: visitor(Data(first.value + second.value)))()  # noqa: PLC3002

    class StoreResultVisitor:
        def __init__(self):
            self.result = None

        def __call__(self, data):
            self.result = data.value

    store = StoreResultVisitor()

    m.add2(Data(1), Data(2), Adder(), store)
    assert store.result == 3

    # without lambda in Adder class, this function fails with
    # RuntimeError: Tried to call pure virtual function "AdderBase::__call__"
    m.add3(Data(1), Data(2), Data(3), Adder(), store)
    assert store.result == 6

