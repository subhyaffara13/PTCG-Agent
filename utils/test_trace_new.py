
def test_trace_new():
    a, b, c, d, Y = symbols('a b c d Y')
    A, B, C, D = symbols('A B C D', commutative=False)

    assert Tr(a + b) == a + b
    assert Tr(A + B) == Tr(A) + Tr(B)

    #check trace args not implicitly permuted
    assert Tr(C*D*A*B).args[0].args == (C, D, A, B)

    # check for mul and adds
    assert Tr((a*b) + ( c*d)) == (a*b) + (c*d)
    # Tr(scalar*A) = scalar*Tr(A)
    assert Tr(a*A) == a*Tr(A)
    assert Tr(a*A*B*b) == a*b*Tr(A*B)

    # since A is symbol and not commutative
    assert isinstance(Tr(A), Tr)

    #POW
    assert Tr(pow(a, b)) == a**b
    assert isinstance(Tr(pow(A, a)), Tr)

    #Matrix
    M = Matrix([[1, 1], [2, 2]])
    assert Tr(M) == 3

    ##test indices in different forms
    #no index
    t = Tr(A)
    assert t.args[1] == Tuple()

    #single index
    t = Tr(A, 0)
    assert t.args[1] == Tuple(0)

    #index in a list
    t = Tr(A, [0])
    assert t.args[1] == Tuple(0)

    t = Tr(A, [0, 1, 2])
    assert t.args[1] == Tuple(0, 1, 2)

    #index is tuple
    t = Tr(A, (0))
    assert t.args[1] == Tuple(0)

    t = Tr(A, (1, 2))
    assert t.args[1] == Tuple(1, 2)

    #trace indices test
    t = Tr((A + B), [2])
    assert t.args[0].args[1] == Tuple(2) and t.args[1].args[1] == Tuple(2)

    t = Tr(a*A, [2, 3])
    assert t.args[1].args[1] == Tuple(2, 3)

    #class with trace method defined
    #to simulate numpy objects
    class Foo:
        def trace(self):
            return 1
    assert Tr(Foo()) == 1

    #argument test
    # check for value error, when either/both arguments are not provided
    raises(ValueError, lambda: Tr())
    raises(ValueError, lambda: Tr(A, 1, 2))

