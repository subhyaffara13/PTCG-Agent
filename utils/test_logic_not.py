
def test_logic_not():
    assert Not('a') != '!a'
    assert Not('!a') != 'a'
    assert Not(True) == False
    assert Not(False) == True

    # NOTE: we may want to change default Not behaviour and put this
    # functionality into some method.
    assert Not(And('a', 'b')) == Or(Not('a'), Not('b'))
    assert Not(Or('a', 'b')) == And(Not('a'), Not('b'))

    raises(ValueError, lambda: Not(1))

