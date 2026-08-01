
def test_issue_5284():
    A, B = symbols('A B', commutative=False)
    assert (x*A).subs(x**2*A, B) == x*A
    assert (A**2).subs(A**3, B) == A**2
    assert (A**6).subs(A**3, B) == B**2

