
def test_lex_order():
    assert lex((1, 2, 3)) == (1, 2, 3)
    assert str(lex) == 'lex'

    assert lex((1, 2, 3)) == lex((1, 2, 3))

    assert lex((2, 2, 3)) > lex((1, 2, 3))
    assert lex((1, 3, 3)) > lex((1, 2, 3))
    assert lex((1, 2, 4)) > lex((1, 2, 3))

    assert lex((0, 2, 3)) < lex((1, 2, 3))
    assert lex((1, 1, 3)) < lex((1, 2, 3))
    assert lex((1, 2, 2)) < lex((1, 2, 3))

    assert lex.is_global is True
    assert lex == LexOrder()
    assert lex != grlex

