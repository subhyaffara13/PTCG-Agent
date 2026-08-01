
def test_issue_7547():
    A, B, V = symbols('A,B,V')
    eq1 = Eq(630.26*(V - 39.0)*V*(V + 39) - A + B, 0)
    eq2 = Eq(B, 1.36*10**8*(V - 39))
    eq3 = Eq(A, 5.75*10**5*V*(V + 39.0))
    sol = Matrix(nsolve(Tuple(eq1, eq2, eq3), [A, B, V], (0, 0, 0)))
    assert str(sol) == str(Matrix(
        [['4442890172.68209'],
         ['4289299466.1432'],
         ['70.5389666628177']]))

