
def test_igcd2():
    # short loop
    assert igcd2(2**100 - 1, 2**99 - 1) == 1
    # Lehmer's algorithm
    a, b = int(fibonacci(10001)), int(fibonacci(10000))
    assert igcd2(a, b) == 1

