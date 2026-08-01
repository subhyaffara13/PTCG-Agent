
def test_satisfiable_bool():
    from sympy.core.singleton import S
    assert satisfiable(true) == {true: true}
    assert satisfiable(S.true) == {true: true}
    assert satisfiable(false) is False
    assert satisfiable(S.false) is False

