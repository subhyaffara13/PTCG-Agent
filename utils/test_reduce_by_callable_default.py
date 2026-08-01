
def test_reduce_by_callable_default():
    def set_add(s, i):
        s.add(i)
        return s

    assert reduceby(iseven, set_add, [1, 2, 3, 4, 1, 2], set) == \
        {True: {2, 4}, False: {1, 3}}

