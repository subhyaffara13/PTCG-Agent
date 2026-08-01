
def test_minisat22_minimal_satisfiable():
    A, B, C = symbols('A,B,C')
    minisat22_satisfiable = lambda expr, minimal=True: satisfiable(expr, algorithm="minisat22", minimal=True)
    assert minisat22_satisfiable( A & ~A ) is False
    assert minisat22_satisfiable( A & ~B ) == {A: True, B: False}
    assert minisat22_satisfiable(
        A | B ) in ({A: True}, {B: False}, {A: False, B: True}, {A: True, B: True}, {A: True, B: False})
    assert minisat22_satisfiable(
        (~A | B) & (~B | A) ) in ({A: True, B: True}, {A: False, B: False})
    assert minisat22_satisfiable( (A | B) & (~B | C) ) in ({A: True, B: False, C: True},
        {A: True, B: True, C: True}, {A: False, B: True, C: True}, {A: True, B: False, C: False})
    assert minisat22_satisfiable( A & B & C  ) == {A: True, B: True, C: True}
    assert minisat22_satisfiable( (A | B) & (A >> B) ) in ({B: True, A: False},
        {B: True, A: True})
    assert minisat22_satisfiable( Equivalent(A, B) & A ) == {A: True, B: True}
    assert minisat22_satisfiable( Equivalent(A, B) & ~A ) == {A: False, B: False}
    g = satisfiable((A | B | C),algorithm="minisat22",minimal=True,all_models=True)
    sol = next(g)
    first_solution = {key for key, value in sol.items() if value}
    sol=next(g)
    second_solution = {key for key, value in sol.items() if value}
    sol=next(g)
    third_solution = {key for key, value in sol.items() if value}
    assert not first_solution <= second_solution
    assert not second_solution <= third_solution
    assert not first_solution <= third_solution

