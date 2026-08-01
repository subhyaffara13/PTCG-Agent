
def test_euler_odd():
    n = Symbol('n', odd=True, positive=True)
    assert euler(n) == 0
    n = Symbol('n', odd=True)
    assert euler(n) != 0

