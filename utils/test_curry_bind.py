
def test_curry_bind():
    @curry
    def add(x=1, y=2):
        return x + y
    assert add() == add(1, 2)
    assert add.bind(10)(20) == add(10, 20)
    assert add.bind(10).bind(20)() == add(10, 20)
    assert add.bind(x=10)(y=20) == add(10, 20)
    assert add.bind(x=10).bind(y=20)() == add(10, 20)

