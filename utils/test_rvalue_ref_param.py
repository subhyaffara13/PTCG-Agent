
def test_rvalue_ref_param():
    r = m.RValueRefParam()
    assert r.func1("123") == 3
    assert r.func2("1234") == 4
    assert r.func3("12345") == 5
    assert r.func4("123456") == 6

