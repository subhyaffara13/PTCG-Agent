
def test_switch():
    def key(x: int) -> int:
        return x % 3

    rl = switch(key, {0: inc, 1: dec})
    assert rl(3) == 4
    assert rl(4) == 3
    assert rl(5) == 5

