
def test_globals():
    def f():
        a
        def g():
            b
            def h():
                c
    assert globalvars(f) == dict(a=1, b=2, c=3)

    res = globalvars(foo, recurse=True)
    assert set(res) == set(['squared', 'a'])
    res = globalvars(foo, recurse=False)
    assert res == {}
    zap = foo(2)
    res = globalvars(zap, recurse=True)
    assert set(res) == set(['squared', 'a'])
    res = globalvars(zap, recurse=False)
    assert set(res) == set(['squared'])
    del zap
    res = globalvars(squared)
    assert set(res) == set(['a'])

