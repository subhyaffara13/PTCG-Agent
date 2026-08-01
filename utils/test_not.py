
def test_not():
    x = Symbol('x')

    r1 = x > -1
    r2 = x <= -1

    i = interval

    f1 = experimental_lambdify((x,), r1)
    f2 = experimental_lambdify((x,), r2)

    tt = i(-0.1, 0.1, is_valid=True)
    tn = i(-0.1, 0.1, is_valid=None)
    tf = i(-0.1, 0.1, is_valid=False)

    assert f1(tt) == ~f2(tt)
    assert f1(tn) == ~f2(tn)
    assert f1(tf) == ~f2(tf)

    nt = i(0.9, 1.1, is_valid=True)
    nn = i(0.9, 1.1, is_valid=None)
    nf = i(0.9, 1.1, is_valid=False)

    assert f1(nt) == ~f2(nt)
    assert f1(nn) == ~f2(nn)
    assert f1(nf) == ~f2(nf)

    ft = i(1.9, 2.1, is_valid=True)
    fn = i(1.9, 2.1, is_valid=None)
    ff = i(1.9, 2.1, is_valid=False)

    assert f1(ft) == ~f2(ft)
    assert f1(fn) == ~f2(fn)
    assert f1(ff) == ~f2(ff)

