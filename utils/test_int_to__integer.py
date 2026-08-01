
def test_int_to_Integer():
    assert int_to_Integer("1 + 2.2 + 0x3 + 40") == \
        'Integer (1 )+2.2 +Integer (0x3 )+Integer (40 )'
    assert int_to_Integer("0b101") == 'Integer (0b101 )'
    assert int_to_Integer("ab1 + 1 + '1 + 2'") == "ab1 +Integer (1 )+'1 + 2'"
    assert int_to_Integer("(2 + \n3)") == '(Integer (2 )+\nInteger (3 ))'
    assert int_to_Integer("2 + 2.0 + 2j + 2e-10") == 'Integer (2 )+2.0 +2j +2e-10 '


def test_int_to_Integer():
    # XXX: Warning, don't test with == here.  0.5 == Rational(1, 2) is True!
    app = init_ipython_session()
    app.run_cell("from sympy import Integer")
    app.run_cell("a = 1")
    assert isinstance(app.user_ns['a'], int)

    enable_automatic_int_sympification(app)
    app.run_cell("a = 1/2")
    assert isinstance(app.user_ns['a'], Rational)
    app.run_cell("a = 1")
    assert isinstance(app.user_ns['a'], Integer)
    app.run_cell("a = int(1)")
    assert isinstance(app.user_ns['a'], int)
    app.run_cell("a = (1/\n2)")
    assert app.user_ns['a'] == Rational(1, 2)

