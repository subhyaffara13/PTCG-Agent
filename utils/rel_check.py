
def rel_check(a, b):
    from sympy.testing.pytest import raises
    assert a.is_number and b.is_number
    for do in range(len({type(a), type(b)})):
        if S.NaN in (a, b):
            v = [(a == b), (a != b)]
            assert len(set(v)) == 1 and v[0] == False
            assert not (a != b) and not (a == b)
            assert raises(TypeError, lambda: a < b)
            assert raises(TypeError, lambda: a <= b)
            assert raises(TypeError, lambda: a > b)
            assert raises(TypeError, lambda: a >= b)
        else:
            E = [(a == b), (a != b)]
            assert len(set(E)) == 2
            v = [
            (a < b), (a <= b), (a > b), (a >= b)]
            i = [
            [True,    True,     False,   False],
            [False,   True,     False,   True], # <-- i == 1
            [False,   False,    True,    True]].index(v)
            if i == 1:
                assert E[0] or (a.is_Float != b.is_Float) # ugh
            else:
                assert E[1]
        a, b = b, a
    return True

