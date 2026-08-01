
def test_nargs_inheritance():
    class f1(Function):
        nargs = 2
    class f2(f1):
        pass
    class f3(f2):
        pass
    class f4(f3):
        nargs = 1,2
    class f5(f4):
        pass
    class f6(f5):
        pass
    class f7(f6):
        nargs=None
    class f8(f7):
        pass
    class f9(f8):
        pass
    class f10(f9):
        nargs = 1
    class f11(f10):
        pass
    assert f1.nargs == FiniteSet(2)
    assert f2.nargs == FiniteSet(2)
    assert f3.nargs == FiniteSet(2)
    assert f4.nargs == FiniteSet(1, 2)
    assert f5.nargs == FiniteSet(1, 2)
    assert f6.nargs == FiniteSet(1, 2)
    assert f7.nargs == S.Naturals0
    assert f8.nargs == S.Naturals0
    assert f9.nargs == S.Naturals0
    assert f10.nargs == FiniteSet(1)
    assert f11.nargs == FiniteSet(1)

