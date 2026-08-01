
def test_Add_queries():
    assert ask(Q.prime(12345678901234567890 + (cos(1)**2 + sin(1)**2))) is True
    assert ask(Q.even(Add(S(2), S(2), evaluate=False))) is True
    assert ask(Q.prime(Add(S(2), S(2), evaluate=False))) is False
    assert ask(Q.integer(Add(S(2), S(2), evaluate=False))) is True

