
def test_recursive_function():
    global fib
    fib2 = copy(fib, recurse=True)
    fib3 = copy(fib)
    fib4 = fib
    del fib
    assert fib2(5) == 5
    for _fib in (fib3, fib4):
        try:
            _fib(5)
        except Exception:
            # This is expected to fail because fib no longer exists
            pass
        else:
            raise AssertionError("Function fib shouldn't have been found")
    fib = fib4

