
def test_M6():
    assert set(solveset(x**7 - 1, x)) == \
        {cos(n*pi*R(2, 7)) + I*sin(n*pi*R(2, 7)) for n in range(0, 7)}

