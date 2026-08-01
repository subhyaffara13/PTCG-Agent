
def test_dpll_satisfiable():
    A, B, C = symbols('A,B,C')
    assert dpll_satisfiable( A & ~A ) is False
    assert dpll_satisfiable( A & ~B ) == {A: True, B: False}
    assert dpll_satisfiable(
        A | B ) in ({A: True}, {B: True}, {A: True, B: True})
    assert dpll_satisfiable(
        (~A | B) & (~B | A) ) in ({A: True, B: True}, {A: False, B: False})
    assert dpll_satisfiable( (A | B) & (~B | C) ) in ({A: True, B: False},
            {A: True, C: True}, {B: True, C: True})
    assert dpll_satisfiable( A & B & C  ) == {A: True, B: True, C: True}
    assert dpll_satisfiable( (A | B) & (A >> B) ) == {B: True}
    assert dpll_satisfiable( Equivalent(A, B) & A ) == {A: True, B: True}
    assert dpll_satisfiable( Equivalent(A, B) & ~A ) == {A: False, B: False}

