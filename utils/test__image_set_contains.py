
def test_ImageSet_contains():
    assert (2, S.Half) in imageset(x, (x, 1/x), S.Integers)
    assert imageset(x, x + I*3, S.Integers).intersection(S.Reals) is S.EmptySet
    i = Dummy(integer=True)
    q = imageset(x, x + I*y, S.Integers).intersection(S.Reals)
    assert q.subs(y, I*i).intersection(S.Integers) is S.Integers
    q = imageset(x, x + I*y/x, S.Integers).intersection(S.Reals)
    assert q.subs(y, 0) is S.Integers
    assert q.subs(y, I*i*x).intersection(S.Integers) is S.Integers
    z = cos(1)**2 + sin(1)**2 - 1
    q = imageset(x, x + I*z, S.Integers).intersection(S.Reals)
    assert q is not S.EmptySet

