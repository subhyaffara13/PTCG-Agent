
def test_do_one():
    rl = do_one(posdec, posdec)
    assert rl(5) == 4

    def rl1(x: int) -> int:
        if x == 1:
            return 2
        return x

    def rl2(x: int) -> int:
        if x == 2:
            return 3
        return x

    rule = do_one(rl1, rl2)
    assert rule(1) == 2
    assert rule(rule(1)) == 3


def test_do_one():
    def bad(expr):
        raise ValueError

    assert list(do_one(inc)(3)) == [4]
    assert list(do_one(inc, bad)(3)) == [4]
    assert list(do_one(inc, posdec)(3)) == [4]

