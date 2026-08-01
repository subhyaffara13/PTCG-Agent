
def test_logic_eval_TF():
    assert And(F, F) == F
    assert And(F, T) == F
    assert And(T, F) == F
    assert And(T, T) == T

    assert Or(F, F) == F
    assert Or(F, T) == T
    assert Or(T, F) == T
    assert Or(T, T) == T

    assert And('a', T) == 'a'
    assert And('a', F) == F
    assert Or('a', T) == T
    assert Or('a', F) == 'a'

