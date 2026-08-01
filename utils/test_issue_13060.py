
def test_issue_13060():
    A, B = symbols("A B", cls=Function)
    t = Symbol("t")
    eq = [Eq(Derivative(A(t), t), A(t)*B(t)), Eq(Derivative(B(t), t), A(t)*B(t))]
    sol = dsolve(eq)
    assert checkodesol(eq, sol) == (True, [0, 0])

