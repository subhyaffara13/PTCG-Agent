
def test_tick_equality(cls, n, m):
    assume(m != n)
    # tick == tock iff tick.n == tock.n
    left = cls(n)
    right = cls(m)
    assert left != right

    right = cls(n)
    assert left == right
    assert not left != right

    if n != 0:
        assert cls(n) != cls(-n)

