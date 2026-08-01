
def test_T13():
    x = symbols('x', real=True)
    assert [limit(x/abs(x), x, 0, dir='-'),
            limit(x/abs(x), x, 0, dir='+')] == [-1, 1]

